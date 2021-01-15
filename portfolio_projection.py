def invest(starting_amount, cagr, num_years, beginning_year=0, annual_topup=0, topup_years=0):
    """Calculate and plot the value of an investment portfolio over time
    Args:
        starting_amount(float): the initial amount to be invested
        
        cagr(float): the Compound Annual Growth Rate (CAGR). This is the annual rate of growth an investment is expected to generate. If CAGR = 25 and starting_amount = 100, then after 1 year your nominal ROI will be 25% and the value of your portfolio will be 125. After 3 years your nominal ROI will be 95% and the value of your portfolio will be 195 (100*(1.25**3)). 
        
        num_years(int): the number of years you intend to invest
        
        beginning_year(int, optional): the tax year you intend to make the initial investment. If not input, then the next tax year will be used. E.g. if the current date is Dec 2020, tax year of April 2021 - April 2022 will be used.  
        
        annual_topup(float, optional): any additional funds to be added to the portfolio on an annual basis, at the start of each tax year. These will be added for topup_years. 
        
        topup_years(int, optional): the number of years after beginning_year that the annual_topup amount will be added to the portfolio. E.g. if beginning_year = 2021, annual_topup = 1000 and topup_years = 4, than (£)1000 will be added to the overall value of your portfolio at the start of 2022, 2023, 2024 and 2025. 
    
    Returns:
        results: a list containing a list of each of the below:
                 1. The years over which the portfolio is held 
                 2. The cumulative value of the portfolio at the end of the given tax year
                 3. The interest earned
                 4. The tax paid 
                 5. The total amount of money invested 
             
        Assumptions:
            * The tax-free allowance for capital gains tax is £12500
            * The tax rate above the tax-free threshold is 40%
            * Capital gains tax: 
                We assume that we sell some fraction of our portfolio each year (and reinvest it in different shares). The amount of capital gains tax will 
                depend on the return on investment(ROI). This in turn will depend on the average age of the shares sold and the input IRR. We assume we sell 20% of our portfolio every year, selling oldest shares first. Under this assumption, for the first 5 years the age of the stocks sold is the number of years since the starting year, and after 5 years the age of any stocks will always be 5 years. E.g. if you have 5 shares, then at the end of each year:
                        Year 1      Year 2      Year 3      Year 4      Year 5      Year 6      Year 7       ...          
                --------------------------------------------------------------------------------------------------         
                          1(sold)     1           2            3          4           5(sold)     1          
                          1           2(sold)     1            2          3           4           5(sold)    
                age       1           2           3(sold)      1          2           3           4          ...
                          1           2           3            4(sold)    1           2           3          
                          1           2           3            4          5(sold)     1           2          
                --------------------------------------------------------------------------------------------------            
                age_sold  1           2           3            4          5           5           5          ...    
                
    """

    # We define some constants and convert the interest rate from a percentage to a decimal  
    fraction_sold = 0.20 # 20% 
    tax_rate = 0.4 # 40% 
    cagr = cagr / 100    


    # If beginning_year provided use it. If not, use next tax year.
    if beginning_year == 0:
        # beginning_year not provided so assume investment begins on next tax year
        from datetime import datetime
        now = datetime.now()
        year = now.year 
        month = now.month     
        if month < 4:
            beginning_year = year 
        else:
            beginning_year = year + 1

    # The user may add funds annually to their portfolio for first few years, as determined by topup_years
    if num_years > topup_years:
        topup = 0
    else:
        topup = annual_topup 

    # Recursively calculate the portfolio value, compound annual growth and tax after each year
    if num_years == 0:
        # Define empty arrays that will be used to store the results
        result_year = []
        result_value = []
        result_growth = []
        result_tax = []
        result_invested = []

        # Append the starting values
        # We will plot the amounts at the end of each tax year but this means the starting_amount doesn't show up on our graph. This might be confusing so we will add another data point representing the end of beginning_year - 1 (aka the start of beginning_year).  
        result_year.append(beginning_year - 1)
        result_value.append(starting_amount)
        result_growth.append(0)
        result_tax.append(0)
        result_invested.append(starting_amount)

        # Calculate the interest and the total value of the portfolio at the end of the current year
        comp_annual_growth = round(starting_amount * cagr)
        value_year_end = starting_amount + comp_annual_growth
        
        # Calculate the capital gains tax that must be paid
        value_sold = (fraction_sold*value_year_end) # Assume fraction_sold % of our portfolio is sold this year
        profit = value_sold-(value_sold/(1+cagr)) 

        if profit > 12500:
            tax_liable = round((profit-12500)*tax_rate) 
            # We assume we pay the tax from our interest, so we must deduct the tax from the comp_annual_growth and value_year_end  
            comp_annual_growth = comp_annual_growth - tax_liable 
            value_year_end = value_year_end - tax_liable 
        else:
            tax_liable = 0   

        # Append the results to our results array and return the array 
        result_year.append(beginning_year)
        result_value.append(value_year_end)
        result_growth.append(comp_annual_growth)
        result_tax.append(tax_liable)
        result_invested.append(starting_amount)

        # Make a list of or result lists
        results = [result_year,result_value,result_growth,result_tax,result_invested]

    elif num_years > 0:
        # Find the total value of our portfolio to date 
        results = invest(starting_amount, (cagr*100), (num_years - 1), beginning_year, annual_topup, topup_years)
        result_year = results[0]
        result_value = results[1] 
        result_growth = results[2]
        result_tax = results[3]
        result_invested = results[4]

        # Calculate the interest and the total value of the portfolio at the end of the current year
        value_year_start = result_value[-1] # The latest element in result_value will the portfolio value to date
        value_year_start = value_year_start + topup # Add the topup amount if there is one this year
        value_year_end = round(value_year_start * (1 + cagr))
        comp_annual_growth = value_year_end - value_year_start         

        # Calculate the capital gains tax that must be paid
        value_sold = (fraction_sold*value_year_end) # Assume fraction_sold % of our portfolio is sold this year

        if num_years >= 5:
            # After 5 years the average age of your stocks will stabilise to 3.8 years assuming you sell 20% of your stocks each year, selling oldest first 
            age = 5
        else:
            # Assume average age of stocks is 2 years
            age = num_years

        profit = value_sold-(value_sold/((1+cagr)**age)) 

        if profit > 12500:
            tax_liable = round((profit-12500)*tax_rate) 
            # We assume we pay the tax from our interest, so we must deduct the tax from the comp_annual_growth and value_year_end  
            comp_annual_growth = comp_annual_growth - tax_liable 
            value_year_end = value_year_end - tax_liable 
        else:
            tax_liable = 0   

        if num_years > topup_years:
            invested_amount = starting_amount + ((topup_years)*annual_topup) 
        else:
            invested_amount = starting_amount + ((num_years)*annual_topup) 

        # Append the results to our results array and return the array 
        year_now = result_year[-1] + 1
        result_year.append(year_now)
        result_value.append(value_year_end)
        result_growth.append(comp_annual_growth)
        result_tax.append(tax_liable)
        result_invested.append(invested_amount)

        results = [result_year,result_value,result_growth,result_tax,result_invested] 

    return results

def plot_returns(results):
    """Plot the results of the output of the 'invest' function
    Args:
        results(list): a list of lists as output by the 'invest' function  
    """   
    import plotly.graph_objects as go
    #import plotly.express as px

    fig = go.Figure()

    result_year = results[0]
    result_value = results[1] 
    result_growth = results[2]
    result_tax = results[3]
    result_invested = results[4]

    # Add traces
    fig.add_trace(go.Scatter(x=result_year, y=result_value,
                        mode='lines+markers',
                        name='Portfolio Value'))
    fig.add_trace(go.Scatter(x=result_year, y=result_growth,
                        mode='lines+markers',
                        name='Compound Annual Growth'))
    fig.add_trace(go.Scatter(x=result_year, y=result_tax,
                        mode='lines+markers',
                        name='Tax Deducted'))
    fig.add_trace(go.Scatter(x=result_year, y=result_invested,
                        mode='lines',
                        name='Amount Invested'))
                        
    # Add Labels
    # Add start and end years to the title
    starting = result_year[0]
    ending = result_year[-1]             
    title = f"Investment Portfolio Performance (April {starting} - April {ending})"  
    x_axis_config = {'title': 'Year', 'dtick': 1}   
    y_axis_config = {'title': 'Amount (£)'}

    fig.update_layout(
        title_text=title,
        xaxis=x_axis_config,
        yaxis=y_axis_config,
    )
    #fig.write_html("investment_plot.html")
    return(fig.to_html(full_html=False, default_height=700, default_width=1000))
    #fig.show()

def plot_upper_lower_bound_returns(years, expected_value, upper_bound, lower_bound):
    """Plot the results of the output of the 'invest' function
    Args:
        years(list): the years your portfolio will be active 
        expected_value(list): the value of the portfolio for these years
        upper_bound(list): the upper bound of your portfolio value
        lower_bound(list): the lower bound of your portfolio value
    """   
    import plotly.graph_objects as go

    fig = go.Figure()

    # Add traces
    fig.add_trace(go.Scatter(x=years, y=upper_bound,
                        mode='lines',
                        name='Upper Bound'))
    fig.add_trace(go.Scatter(x=years, y=lower_bound,
                        mode='lines',
                        name='Lower Bound',
                        fill='tonexty'))
    fig.add_trace(go.Scatter(x=years, y=expected_value,
                        mode='lines+markers',
                        name='Expected Value'))
                        
    # Add Labels
    # Add start and end years to the title
    starting = years[0]
    ending = years[-1]             
    title = f"Investment Portfolio Performance (April {starting} - April {ending})"  
    x_axis_config = {'title': 'Year', 'dtick': 1}   
    y_axis_config = {'title': 'Amount (£)'}

    fig.update_layout(
        title_text=title,
        xaxis=x_axis_config,
        yaxis=y_axis_config,
    )
    return(fig.to_html(full_html=False, default_height=700, default_width=1000))  