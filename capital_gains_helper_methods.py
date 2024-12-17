from stock_ledger import StockLedger
from random import SystemRandom


def display_interpret_string_as_ledger(input_str: str, display: bool =False) -> StockLedger:  # O(N)
    sl = StockLedger()
    input_lines = input_str.split('\n')
    for each_line in input_lines:  # O(N=len(input_lines))
        each_split_line = each_line.split()  # splits on spaces
        # print(each_line)
        if each_line.count('Display') == 0:
            price_string = each_split_line[-1].strip('.$')
        if each_split_line[0] == 'Buy':
            sl.buy(each_split_line[4], int(each_split_line[1]), float(price_string))
        elif each_split_line[0] == 'Sell':
            sl.sell(each_split_line[4], int(each_split_line[1]), float(price_string))
        elif display:
            sl.display_ledger()
    return sl
    

def interpret_string_as_ledger(input_str: str) -> StockLedger:  # O(N)
    return display_interpret_string_as_ledger(input_str)


# def string_to_trading_bot(input_str: str, trading_bot: TradingBot, strategy_selection_int: int=1) -> tuple[list[int], list[float]]:  # O(1) or O(f(N))
#     """strategy_selection_int:\n\n1: sell\n\n2: sellRandom\n\n3: sellOptimal() (sell lowest cost shares first)\n\n4: sellOptimal(optimal_selection_int=2) (sell below the median (per round of the deque))"""
#     input_lines = input_str.split('\n')  #                       # O(f(N))
#     plot_x = []
#     plot_y = []
#     for each_line in input_lines:  # O(N=len(input_lines))
#         # plot_x.append(len(plot_x))  # on list, O(1)
#         # plot_y.append(trading_bot.report_profit())
#         each_split_line = each_line.split()  # splits on spaces
#         if each_line.count('Display') == 0:
#             price_string = each_split_line[-1].strip('.$')
#         else:
#             trading_bot.stock_ledger.display_ledger()
#         if each_split_line[0] == 'Buy':
#             trading_bot.buy(each_split_line[4], int(each_split_line[1]), float(price_string))
#         elif each_split_line[0] == 'Sell':
#             if strategy_selection_int == 1:
#                 trading_bot.sell(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(1) * O(num shares)
#             elif strategy_selection_int == 2:
#                 trading_bot.sellRandom(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(len(entry)) * O(num shares)
#             elif strategy_selection_int == 3:
#                 trading_bot.sellOptimal(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(f(N))
#             elif strategy_selection_int == 4:
#                 trading_bot.sellOptimal(each_split_line[4], int(each_split_line[1]), float(price_string), 2)  # O(f(N))
#             plot_x.append(len(plot_x))  # O(N=len(list))  # track sales
#             plot_y.append(trading_bot.last_profit())
#     return plot_x, plot_y

# def string_to_random_trading_bot(input_str: str, trading_bot: TradingBot) -> tuple[list[int], list[float]]:  # O(N) (more shares, more deque movement as f(N))
#     input_lines = input_str.split('\n')  #                       # O(f(N))
#     plot_x = []
#     plot_y = []
#     for each_line in input_lines:  # O(N=len(input_lines))
#         # plot_x.append(len(plot_x))  # O(N=len(list))
#         # plot_y.append(trading_bot.report_profit())
#         each_split_line = each_line.split()  # splits on spaces
#         if each_line.count('Display') == 0:
#             price_string = each_split_line[-1].strip('.$')
#         if each_split_line[0] == 'Buy':
#             trading_bot.buy(each_split_line[4], int(each_split_line[1]), float(price_string))
#         elif each_split_line[0] == 'Sell':
#             trading_bot.sellRandom(each_split_line[4], int(each_split_line[1]), float(price_string))  # O(1) * O(num shares)
#             plot_x.append(len(plot_x))  # O(N=len(list))  # track sales
#             plot_y.append(trading_bot.report_last_profit())
#     return plot_x, plot_y

# def string_to_optimal_trading_bot(input_str: str, trading_bot: TradingBot, optimal_selection_int: int) -> tuple[list[int], list[float]]:
#     input_lines = input_str.split('\n')  #                       # O(f(N))
#     plot_x = []
#     plot_y = []
#     for each_line in input_lines:  # O(N=len(input_lines))
#         # plot_x.append(len(plot_x))  # on list, O(1)
#         # plot_y.append(trading_bot.report_profit())
#         each_split_line = each_line.split()  # splits on spaces
#         if each_line.count('Display') == 0:
#             price_string = each_split_line[-1].strip('.$')
#         if each_split_line[0] == 'Buy':
#             trading_bot.buy(each_split_line[4], int(each_split_line[1]), float(price_string))
#         elif each_split_line[0] == 'Sell':
#             trading_bot.sellOptimal(each_split_line[4], int(each_split_line[1]), float(price_string), optimal_selection_int)  # O(f(N))
#             plot_x.append(len(plot_x))  # O(N=len(list))  # track sales
#             plot_y.append(trading_bot.report_last_profit())
#     return plot_x, plot_y


def get_buy_sell_line(stock_symbol: str, buy_sell_str: str, quantity: int, price: float) -> str:  # O(1)
    # ex: "Buy 20 shares of AAPL at $45."
    return str(f"{buy_sell_str} {quantity} shares of {stock_symbol} at ${price}.")


def generate_buy_sell_lines_string(stock_symbols: list[str],
                                   number_of_transactions: int, minimum_quantity: int=1,
                                   maximum_quantity: int=100) -> tuple[str, list[int]]:  # O(N)
    """This assumes some market conditions:
    NVDA goes up.
    As a counter gets above 200, Microsoft starts to go up (before that, it goes down).
    No price is greater than 400."""
    # returned list is in order of stock_symbols, which comes from client code (for example, likely will not match order in a StockLedger)
    gbss_shares_quantity_list = [0 for gbss_i in range(len(stock_symbols))]
    gbss_line_list = []
    # for nt_i in range(number_of_transactions):  # actually, could use this definite loop
    counter = 0
    while len(gbss_line_list) < number_of_transactions:  # O(N=number_of_transactions)
        counter += 1
        a_symbol = SystemRandom().choice(stock_symbols)
        a_quantity = SystemRandom().randrange(minimum_quantity, maximum_quantity + 1)
        if a_symbol == 'NVDA':
            a_price = round((100 + counter) * (SystemRandom().random() + SystemRandom().random()), 2)
        elif a_symbol == 'MSFT':
            a_price = round(SystemRandom().random() * 200 * (abs(200 - counter) / 200), 2)
        else:
            a_price = SystemRandom().randrange(150, 351)
        a_price = min(a_price, 400)
        # if a quantity is more than currently held, make it a buy
        if a_quantity > gbss_shares_quantity_list[stock_symbols.index(a_symbol)]:
            a_buy_or_sell = 'Buy'
        else:  # otherwise, choose pseudorandomly
            a_buy_or_sell = SystemRandom().choice(['Buy', 'Sell'])  # could weight this choice with more 'Sell' items, or use a cutoff for a pseudorandom number
        if a_buy_or_sell == 'Buy':
            gbss_shares_quantity_list[stock_symbols.index(a_symbol)] += a_quantity
        # else:  # == 'Sell'
        if a_buy_or_sell == 'Sell':
            gbss_shares_quantity_list[stock_symbols.index(a_symbol)] -= a_quantity
        gbss_line_list.append(get_buy_sell_line(a_symbol, a_buy_or_sell, a_quantity, a_price))
    return '\n'.join(gbss_line_list), gbss_shares_quantity_list  
# For testing, the total shares of each ledger entry resulting from returned str should match returned list[int]

