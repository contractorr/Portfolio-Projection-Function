from eToro_investment import invest

results = invest(starting_amount=2002.0
                ,interest_rate=4
                ,num_years=20
                ,beginning_year=2021
                ,annual_topup=1000.0
                ,topup_years=6)  

print(results[0])
# def invest(starting_amount, annual_topup, interest_rate, num_years, beginning=2021, topup_years=5, method=1):
#     """Function to calculate stock market returns"""

#     # Only topup for first few years, as determined by topup_years
#     if num_years > topup_years:
#         topup = 0
#     else:
#         topup = annual_topup 

#     if num_years < 0:
#         print("The investment period must be at least 1 year")
#     elif num_years == 0:
#         y_end = round(starting_amount * interest_rate)
#         gain = y_end - starting_amount 
#         extracted = 0
#         print(f'April {beginning+ 1} - 1 year elapsed  - \ttotal: {y_end} \tgain: {gain} \tinvested_to_date: {starting_amount} \textracted: 0')
#     elif num_years > 0:
#         # Calculate the total value of our portfolio and the gains we expect to make. 
#         y_start, extracted = invest(starting_amount, annual_topup, interest_rate, (num_years - 1),beginning=2021)
#         y_end = round((y_start + topup) * interest_rate)
#         gain = y_end - y_start

         
#         if method == 1:
#             # The below method assumes we keep all our money in the portfolio and only take out the amount we need to pay capital gains tax each year
#             if gain > 12500: 
#                 tax = round((gain - 12500)*0.4) # Assume 40% tax on anything over 12500
#                 gain = gain - tax # deduct this from the gain 
#                 y_end = y_end - tax # deduct this from the total. Tax will be paid from our earnings. 
#                 extracted = tax # we will extract the tax but nothing else
#             else:
#                 extracted = 0   

#         elif method != 1:
#             # The below is if we decided to not pay any tax and instead siphon off money to keep our gain from ever being greater than £12500 

#             # UK tax free shares capital gains allowance 
#             limit = 12500

#             # logic so that we extract an appropriate amount of money as our gains threaten to overshoot our tax free allowance 
#             if gain > (limit - 3000) and gain <= (limit - 2000):
#                 extract = 5000
#                 y_end = round((y_start-extract)*interest_rate)
#                 extracted += extract
#             elif gain > (limit - 2000) and gain <= (limit - 1000):
#                 extract = 7000
#                 y_end = round((y_start-extract)*interest_rate)
#                 extracted += extract
#             elif gain > (limit - 1000) and gain <= limit:
#                 extract = 9000
#                 y_end = round((y_start-extract)*interest_rate)
#                 extracted += extract
#             elif gain > limit:
#                 extract = gain
#                 y_end = round((y_start-extract)*interest_rate)
#                 extracted += extract
#             else:
#                 y_end = round((y_start + topup) * interest_rate) 

#         if num_years > topup_years:
#             invested = starting_amount + ((num_years)*annual_topup) - ((num_years-topup_years)*annual_topup)
#         else:
#             invested = starting_amount + ((num_years)*annual_topup)    
#         print(f'April {beginning + num_years + 1} - {num_years + 1} years elapsed - total: {y_end} \tgain: {gain} \tinvested_to_date: {invested} \textracted: {extracted}')
    
#     return y_end, extracted
    
# value = invest(5000, 5000, 1.25, 22, 2021, 5)    


# #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def invest(starting_amount, interest_rate, num_years, beginning_year=0, annual_topup=0, topup_years=0):
#     """Calculate and plot the value of an investment portfolio
#     Args:
#         starting_amount(float): the initial amount to be invested
#         interest_rate(float): the average interest rate we will assume will apply for the duration of our investment. E.g. 8% interest should be input as 8. 
#         num_years(int): the number of years you intend to invest
#         beginning_year(int, optional): the tax year you intend to make the initial investment
#         annual_topup(float, optional): any additional funds to be added to the portfolio on an annual basis
#         topup_years(int, optional): the number of years that the annual_topup amount will be added to the portfolio
#     Returns:
#         year:
#         y_end: 
             
#     """


#     # Validate the inputs
#     # starting_amount validations
#     if starting_amount < 0: 
#         print('starting_amount input must be greater than 0') 
#         return None
#     elif not isinstance(starting_amount, int) or isinstance(starting_amount, float):
#         print('starting_amount input must be an integer or float type') 
#         return None
#     # interest_rate validations
#     elif interest_rate <= 0:
#         print('interest_rate input must be greater than 0')
#         return None
#     elif not isinstance(interest_rate, int) or isinstance(interest_rate, float):
#         print('interest_rate input must be an integer or float type') 
#         return None
#     # num_years validations
#     elif num_years < 0:
#         print('num_years input must greater than 0')
#         return None
#     elif not isinstance(num_years, int):
#         print('num_years input must be an integer') 
#         return None
#     # beginning_year validations
#     elif beginning_year != 0 and beginning_year <1900:
#         print('beginning_year must be more recent than 1900')
#         return None
#     elif not isinstance(beginning_year, int):
#         print('beginning_year input must be an integer') 
#         return None
#     # annual_topup validations
#     elif annual_topup <= 0:
#         print('annual_topup input must be greater than 0')
#         return None
#     elif not isinstance(annual_topup, int) or isinstance(annual_topup, float):
#         print('annual_topup input must be an integer or float type') 
#         return None
#     # topup_years validations
#     elif topup_years < 0:
#         print('topup_years input must be greater than 0') 
#         return None
#     elif not isinstance(topup_years, int):
#         print('topup_years input must be an integer') 
#         return None

#     # If beginning_year provided use it. If not, use next tax year.
#     if beginning_year == 0:
#         # beginning_year not provided so assume investment begins on next tax year
#         from datetime import datetime
#         now = datetime.now()
#         year = now.year 
#         month = now.month     
#         if month < 4:
#             beginning_year = year 
#         else:
#             beginning_year = year + 1

#     # The user may add funds annually to their portfolio for first few years, as determined by topup_years
#     if num_years > topup_years:
#         topup = 0
#     else:
#         topup = annual_topup 

#     # Recursively calculate the interest, tax and portfolio value after each year
#     if num_years == 0:
#         # Define empty arrays that will be used to store the results
#         result_year = []
#         result_value = []
#         result_interest = []
#         result_tax = []
#         result_invested = []

#         # Calculate the interest and the total value of the portfolio at the end of the current year
#         value_year_end = round(starting_amount * (1 + (interest_rate / 100)))
#         interest_amount = value_year_end - starting_amount 
        
#         # Calculate the capital gains tax that must be paid
#         if interest_amount > 12500:
#             tax = round((interest_amount - 12500)*0.4) # Assume 40% tax on anything over £12,500
#             # We assume we pay the tax from our interest, so we must deduct the tax from the interest_amount and value_year_end  
#             interest_amount = interest_amount - tax 
#             value_year_end = value_year_end - tax 
#         else:
#             tax = 0   

#         # Append the results to our results array and return the array 
#         result_year.append(beginning_year+1)
#         result_value.append(value_year_end)
#         result_interest.append(interest_amount)
#         result_tax.append(tax)

#         # Make a list of or result lists
#         results = [result_year,result_value,result_interest,result_tax,result_invested]

#     elif num_years > 0:
#         # Find the total value of our portfolio to date 
#         results = invest(starting_amount, interest_rate, (num_years - 1), beginning_year, annual_topup, topup_years)
#         result_year = results[0]
#         result_value = results[1] 
#         result_interest = results[2]
#         result_tax = results[3]
#         result_invested = results[4]

#         # Calculate the interest and the total value of the portfolio at the end of the current year
#         value_year_start = result_value[-1] # The latest element in result_value will the portfolio value to date 
#         value_year_start = value_year_start + topup # Add the topup amount if there is one this year
#         value_year_end = round((value_year_start + topup) * (1 + (interest_rate / 100)))
#         interest_amount = value_year_end - value_year_start         

#         # Calculate the capital gains tax that must be paid
#         if interest_amount > 12500:
#             tax = round((interest_amount - 12500)*0.4) # Assume 40% tax on anything over £12,500
#             # We assume we pay the tax from our interest, so we must deduct the tax from the interest_amount and value_year_end  
#             interest_amount = interest_amount - tax 
#             value_year_end = value_year_end - tax 
#         else:
#             tax = 0   

#         if num_years > topup_years:
#             invested_amount = starting_amount + ((topup_years)*annual_topup) 
#         else:
#             invested_amount = starting_amount + ((num_years)*annual_topup) 

#         # Append the results to our results array and return the array 
#         year_now = result_year[-1] + 1
#         result_year.append(year_now)
#         result_value.append(value_year_end)
#         result_interest.append(interest_amount)
#         result_tax.append(tax)
#         result_invested.append(invested_amount)

#         results = [result_year,result_value,result_interest,result_tax,result_invested] 

#     return results

# results = invest(starting_amount=4500
#                 ,interest_rate=20
#                 ,num_years=20
#                 ,annual_topup=4500
#                 ,topup_years=5)    
    
# print(results[1])    
# import numpy as np
# ones = np.array([[1, 1, 1, 1, 1],
#                  [1, 1, 1, 1, 1],
#                  [1, 1, 1, 1, 1]])
# ones[1:3,2:4] = 0
# print(ones)