"""transform html data to structured data"""
from pandas import DataFrame

def define_type_security(security_name):
    """
    Define the type of security based on the security name.

    Args:
    - security_name: str

    Returns:
    - str
    """
    # Si cualquiera de estas palabras está en el nombre del activo, es un bono
    bonos = ['Bono', 'Bopreal']

    # Si cualquiera de estas palabras está en el nombre del activo, es una Obligacion negociable
    on = ['On', 'Obligacion negociable']

    if any(word in security_name for word in bonos):
        return 'bono'
    if any(word in security_name for word in on):
        return 'obligacion_negociable'

    return 'Instrumento_no_identificado'

def structure_portfolio(html_data):
    """
    Structure the raw portfolio data and save it in a csv file
    on silver layer.

    Side effects:
    - Save the structured portfolio data in a csv file
    """
    df_iol_portfolio = DataFrame(html_data)

    df_iol_portfolio = df_iol_portfolio[
        ["Activo", "Cantidad", "Último precio", "Precio promedio  de compra"]
    ]

    df_iol_portfolio.columns = df_iol_portfolio.columns.droplevel(0)

    # Me quedo con la primera palabra de la columna Activo
    df_iol_portfolio['Activo'] = df_iol_portfolio['Activo'].str.split()
    df_iol_portfolio['Ticket'] = df_iol_portfolio['Activo'].str[0]

    # Elimino el primer elemento de la columna Activo
    df_iol_portfolio['Activo'] = df_iol_portfolio['Activo'].str[1:].str.join(' ')

    columns_ars = ["Precio promedio  de compra", "Último precio"]

    for column in columns_ars:
        df_iol_portfolio[column] = df_iol_portfolio[column].str.replace(
                                    '$', ''
                                ).str.replace(
                                    '.', ''
                                ).str.replace(
                                    ',', '.'
                                ).astype(float)

    df_iol_portfolio = df_iol_portfolio.rename(columns={
        "Activo": "Nombre",
        "Precio promedio  de compra": "PPC",
        "Último precio": "Ultimo Precio"
        })

    df_iol_portfolio['Total'] = df_iol_portfolio['Cantidad'] \
                                         * (df_iol_portfolio['Ultimo Precio'] / 100)

    df_iol_portfolio = df_iol_portfolio[[
        'Ticket', 'Nombre', 'Cantidad', 
        'Ultimo Precio', 'PPC', 'Total'
        ]]

    df_iol_portfolio['Tipo'] = df_iol_portfolio['Nombre'].apply(define_type_security)

    return df_iol_portfolio
