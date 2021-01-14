def invest(starting_amount, interest_rate, num_years, beginning_year=0, annual_topup=0, topup_years=0):
    """Calculate and plot the value of an investment portfolio
    Args:
        starting_amount(float): the initial amount to be invested
        interest_rate(float): the average interest rate we will assume will apply for the duration of our investment. E.g. 8% interest should be input as 8. 
        num_years(int): the number of years you intend to invest
        beginning_year(int, optional): the tax year you intend to make the initial investment
        annual_topup(float, optional): any additional funds to be added to the portfolio on an annual basis, at the start of each tax year
        topup_years(int, optional): the number of years that the annual_topup amount will be added to the portfolio
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
                depend on the profit made on the shares sold. This in turn will depend on the average age of the shares sold. We assume we sell 20% of our 
                portfolio every year, selling oldest shares first. Under this assumption the average age of our shares stabilises after 5 years at 3.8 years.
        
    """
    # Validate the inputs
    # starting_amount validations
    if starting_amount < 0: 
        print('starting_amount input must be greater than 0') 
        return None
    elif not isinstance(starting_amount, int) or isinstance(starting_amount, float):
        print('starting_amount input must be an integer or float type') 
        return None
    # interest_rate validations
    elif interest_rate <= 0:
        print('interest_rate input must be greater than 0')
        return None
    elif not (isinstance(interest_rate, int) or isinstance(interest_rate, float)):
        print('interest_rate input must be an integer or float type') 
        return None
    # num_years validations
    elif num_years < 0:
        print('num_years input must greater than 0')
        return None
    elif not isinstance(num_years, int):
        print('num_years input must be an integer') 
        return None
    # beginning_year validations
    elif beginning_year != 0 and beginning_year <1900:
        print('beginning_year must be more recent than 1900')
        return None
    elif not isinstance(beginning_year, int):
        print('beginning_year input must be an integer') 
        return None
    # annual_topup validations
    elif annual_topup < 0:
        print('annual_topup input must be greater than 0')
        return None
    elif not isinstance(annual_topup, int) or isinstance(annual_topup, float):
        print('annual_topup input must be an integer or float type') 
        return None
    # topup_years validations
    elif topup_years < 0:
        print('topup_years input must be greater than 0') 
        return None
    elif not isinstance(topup_years, int):
        print('topup_years input must be an integer') 
        return None

    # We define some constants and set interest rate to decimal
    fraction_liable = 0.20 # 20% 
    tax_rate = 0.4 # 40% 
    interest_rate = interest_rate / 100    


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

    # Recursively calculate the interest, tax and portfolio value after each year
    if num_years == 0:
        # Define empty arrays that will be used to store the results
        result_year = []
        result_value = []
        result_interest = []
        result_tax = []
        result_invested = []

        # Append the starting values
        # result_year.append(beginning_year)
        # result_value.append(starting_amount)
        # result_interest.append(0)
        # result_tax.append(0)
        # result_invested.append(starting_amount)

        # Calculate the interest and the total value of the portfolio at the end of the current year
        interest_amount = round(starting_amount * interest_rate)
        value_year_end = starting_amount + interest_amount
        
        # Calculate the capital gains tax that must be paid
        value_sold = (fraction_liable*value_year_end) # Assume fraction_liable % of our portfolio is sold this year
        profit = value_sold-(value_sold/(1+interest_rate)) 

        if profit > 12500:
            tax_liable = round((profit-12500)*tax_rate) 
            # We assume we pay the tax from our interest, so we must deduct the tax from the interest_amount and value_year_end  
            interest_amount = interest_amount - tax_liable 
            value_year_end = value_year_end - tax_liable 
        else:
            tax_liable = 0   

        # Append the results to our results array and return the array 
        result_year.append(beginning_year+1)
        result_value.append(value_year_end)
        result_interest.append(interest_amount)
        result_tax.append(tax_liable)
        result_invested.append(starting_amount)

        # Make a list of or result lists
        results = [result_year,result_value,result_interest,result_tax,result_invested]

    elif num_years > 0:
        # Find the total value of our portfolio to date 
        results = invest(starting_amount, (interest_rate*100), (num_years - 1), beginning_year, annual_topup, topup_years)
        result_year = results[0]
        result_value = results[1] 
        result_interest = results[2]
        result_tax = results[3]
        result_invested = results[4]

        # Calculate the interest and the total value of the portfolio at the end of the current year
        value_year_start = result_value[-1] # The latest element in result_value will the portfolio value to date
        value_year_start = value_year_start + topup # Add the topup amount if there is one this year
        value_year_end = round(value_year_start * (1 + interest_rate))
        interest_amount = value_year_end - value_year_start         

        # Calculate the capital gains tax that must be paid
        value_sold = (fraction_liable*value_year_end) # Assume fraction_liable % of our portfolio is sold this year

        if num_years >= 5:
            # After 5 years the average age of your stocks will stabilise to 3.8 years assuming you sell 20% of your stocks each year, selling oldest first 
            average_age = 3.8
        else:
            # Assume average age of stocks is 2 years
            average_age = 2

        profit = value_sold-(value_sold/((1+interest_rate)**average_age)) 

        if profit > 12500:
            tax_liable = round((profit-12500)*tax_rate) 
            # We assume we pay the tax from our interest, so we must deduct the tax from the interest_amount and value_year_end  
            interest_amount = interest_amount - tax_liable 
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
        result_interest.append(interest_amount)
        result_tax.append(tax_liable)
        result_invested.append(invested_amount)

        results = [result_year,result_value,result_interest,result_tax,result_invested] 

    return results

def plot_returns(results):
    """Plot the results of the output of the 'invest' function
    Args:
        results(list): a list of lists as output by the 'invest' function  
    """   
    import plotly.graph_objects as go
    import plotly.express as px

    fig = go.Figure()

    result_year = results[0]
    result_value = results[1] 
    result_interest = results[2]
    result_tax = results[3]
    result_invested = results[4]

    # Add traces
    fig.add_trace(go.Scatter(x=result_year, y=result_value,
                        mode='lines+markers',
                        name='Portfolio Value'))
    fig.add_trace(go.Scatter(x=result_year, y=result_interest,
                        mode='lines+markers',
                        name='Interest After Tax'))
    fig.add_trace(go.Scatter(x=result_year, y=result_tax,
                        mode='lines+markers',
                        name='Tax'))
    fig.add_trace(go.Scatter(x=result_year, y=result_invested,
                        mode='lines',
                        name='Invested'))
                        
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
    fig.show()

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
    fig.show()    