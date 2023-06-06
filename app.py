from flask import Flask, jsonify
import yfinance as yf
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR')

app = Flask(__name__)

@app.route('/cotacoes', methods=['GET'])
def get_cotacoes():
    usd_rate, usd_percent = get_exchange_rate('USD', 'BRL')
    eur_rate, eur_percent = get_exchange_rate('EUR', 'BRL')
    gbp_rate, gbp_percent = get_exchange_rate('GBP', 'BRL')
    btc_rate, btc_percent = get_btc_rate(usd_rate)

    ibovespa_index, ibovespa_percent = get_ibovespa_index() or ('N/A', 'N/A')
    rede_dor_stock_price, rede_dor_percent = get_stock_price('RDOR3.SA') or ('N/A', 'N/A')
    oncoclinicas_stock_price, oncoclinicas_percent = get_stock_price('ONCO3.SA') or ('N/A', 'N/A')
    

    cotacoes = {
        'dolar': {'valor': format_value(usd_rate), 'percentual': format_value(usd_percent)},
        'euro': {'valor': format_value(eur_rate), 'percentual': format_value(eur_percent)},
        'libra': {'valor': format_value(gbp_rate), 'percentual': format_value(gbp_percent)},
        'bitcoin': {'valor': format_value(btc_rate), 'percentual': format_value(btc_percent)},
        'ibovespa': {'valor': format_value(ibovespa_index), 'percentual': format_value(ibovespa_percent)},
        'RDOR3': {'valor': format_value(rede_dor_stock_price), 'percentual': format_value(rede_dor_percent)},
        'ONCO3': {'valor': format_value(oncoclinicas_stock_price), 'percentual': format_value(oncoclinicas_percent)}
        
    }

    return jsonify(cotacoes)

def get_exchange_rate(from_currency, to_currency):
    try:
        ticker = yf.Ticker(f'''{from_currency}{to_currency}=X''')
        exchange_data = ticker.history(period='2d')
        exchange_rate_today = exchange_data['Close'].iloc[-1]
        exchange_rate_yesterday = exchange_data['Close'].iloc[-2]
        exchange_percent = ((exchange_rate_today - exchange_rate_yesterday) / exchange_rate_yesterday) * 100
        return exchange_rate_today, exchange_percent
    except Exception:
        return None, None

def get_btc_rate(usd_rate):
    try:
        ticker = yf.Ticker('BTC-USD')
        btc_data = ticker.history(period='2d')
        # btc_rate_today_usd = btc_data['Close'].iloc[-1]
        # btc_rate_yesterday_usd = btc_data['Close'].iloc[-2]
        # btc_percent_usd = ((btc_rate_today_usd - btc_rate_yesterday_usd) / btc_rate_yesterday_usd) * 100

        btc_rate_today_brl = btc_data['Close'].iloc[-1] * usd_rate
        btc_rate_yesterday_brl = btc_data['Close'].iloc[-2] * usd_rate
        btc_percent_brl = ((btc_rate_today_brl - btc_rate_yesterday_brl) / btc_rate_yesterday_brl) * 100

        return btc_rate_today_brl, btc_percent_brl
    except Exception:
        return None, None

def get_ibovespa_index():
    try:
        ibovespa_ticker = yf.Ticker('^BVSP')
        ibovespa_data = ibovespa_ticker.history(period='2d')
        ibovespa_index_today = ibovespa_data['Close'].iloc[-1]
        ibovespa_index_yesterday = ibovespa_data['Close'].iloc[-2]
        ibovespa_percent = ((ibovespa_index_today - ibovespa_index_yesterday) / ibovespa_index_yesterday) * 100
        return ibovespa_index_today, ibovespa_percent
    except Exception:
        return None, None

def get_stock_price(company):
    try:
        ticker = yf.Ticker(company)
        stock_data = ticker.history(period='2d')
        stock_price_today = stock_data['Close'].iloc[-1]
        stock_price_yesterday = stock_data['Close'].iloc[-2]
        stock_percent = ((stock_price_today - stock_price_yesterday) / stock_price_yesterday) * 100
        return stock_price_today, stock_percent
    except Exception:
        return None, None

def format_value(value):
    if value is not None:
        return float('{:.3f}'.format(value))
    return 'N/A'

@app.route('/', methods=['GET'])
def get_cotacoes_tab():
    usd_rate, usd_percent = get_exchange_rate('USD', 'BRL')
    eur_rate, eur_percent = get_exchange_rate('EUR', 'BRL')
    gbp_rate, gbp_percent = get_exchange_rate('GBP', 'BRL')
    btc_rate, btc_percent = get_btc_rate(usd_rate)

    ibovespa_index, ibovespa_percent = get_ibovespa_index() or ('N/A', 'N/A')
    rede_dor_stock_price, rede_dor_percent = get_stock_price('RDOR3.SA') or ('N/A', 'N/A')
    oncoclinicas_stock_price, oncoclinicas_percent = get_stock_price('ONCO3.SA') or ('N/A', 'N/A')
    rede_materdei_stock_price, rede_materdei_percent = get_stock_price('MATD3.SA') or ('N/A', 'N/A')
    
    
    cotacoes = {
        'Dolar': {'Valor (R$)': format_value(usd_rate), 'Variação (%)': format_value(usd_percent)},
        'Euro': {'Valor (R$)': format_value(eur_rate), 'Variação (%)': format_value(eur_percent)},
        'Libra': {'Valor (R$)': format_value(gbp_rate), 'Variação (%)': format_value(gbp_percent)},
        'Bitcoin': {'Valor (R$)': format_value(btc_rate), 'Variação (%)': format_value(btc_percent)},
        'Ibovespa': {'Valor (R$)': format_value(ibovespa_index), 'Variação (%)': format_value(ibovespa_percent)},
        'RDOR3': {'Valor (R$)': format_value(rede_dor_stock_price), 'Variação (%)': format_value(rede_dor_percent)},
        'ONCO3': {'Valor (R$)': format_value(oncoclinicas_stock_price), 'Variação (%)': format_value(oncoclinicas_percent)},
        'MATD3': {'Valor (R$)': format_value(rede_materdei_stock_price), 'Variação (%)': format_value(rede_materdei_percent)}
    }
    


    html_table = pd.DataFrame.from_dict(cotacoes).T.to_html(classes='table table-dark', justify='center')
    html_table = html_table.replace('<table', '<table style="font-family: Arial; text-align: center;"')
    html_table = html_table.replace('<th>', '<th style="padding: 8px;">')
    html_table = html_table.replace('<td>', '<td style="padding: 8px;">')

    # Adicionar setas verdes para cima e vermelhas para baixo
    for asset in cotacoes.keys():
        if cotacoes[asset]['Variação (%)'] != 'N/A':
            percentual = float(cotacoes[asset]['Variação (%)'])
            if percentual > 0:
                arrow = '<span style="color: lightgreen;">&#9650;</span>'
            elif percentual < 0:
                arrow = '<span style="color: lightcoral;">&#9660;</span>'
            else:
                arrow = ''
            html_table = html_table.replace(f'>{format_value(percentual)}<', f'>{format_value(percentual)} {arrow}<')

    # Iterar sobre as células da tabela HTML e formatar os números
    rows = html_table.split('</tr>')
    for i in range(1, len(rows) - 1):
        cells = rows[i].split('</td>')
        for j in range(0, len(cells) - 1):
            value = cells[j].split('>')[-1]
            try:
                formatted_value = locale.format_string('%.3f', float(value), grouping=True)
                cells[j] = cells[j].replace(value, formatted_value)
            except ValueError:
                pass

        rows[i] = '</td>'.join(cells)

    html_table = '</tr>'.join(rows)
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Cotações</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/css/bootstrap.min.css">
    <style>
        body {{
            background-color: #222;
            color: #fff;
        }}uirements.txt
        .container {{
            margin-top: 50px;
        }}
        .table-dark {{
            background-color: #333;
            color: #fff;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px;
            text-align: center;
        }}
        .footer {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            font-size: 10px;
            color: #999;
        }}
        .logo img {{
            width: 150px; /* Altere o valor de largura para o desejado */
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="https://github.com/iniciativafis/logos/blob/720dd587de67a2a066e77dadebd78672dedb3636/fisAI.png?raw=true">
        </div>
        <h1 style="text-align: center;">Cotações</h1>
        {html_table}
        <br>
        <div style="font-family: Arial; font-size: 12px;">
          <p style="margin-bottom: 0;">* Os valores de referência estão sendo extraídos do Yahoo Finanças</p>
          <p style="margin-bottom: 0;">** As variações são relacionadas ao valor no horário de fechamento da bolsa</p>
        </div>
        <div class="footer">
            Powered by Iniciativa FIS
        </div>
    </div>
</body>
</html>
'''


if __name__ == '__main__':
    app.run()
    
    