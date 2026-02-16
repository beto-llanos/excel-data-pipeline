import pandas as pd
import os
import sys


def load_files(folder):

    files = [f for f in os.listdir(folder) if f.endswith('.xlsx')]

    dfs = []

    for file in files:

        print(f"Loading {file}")

        path = os.path.join(folder, file)

        df = pd.read_excel(path)

        print("Columnas encontradas:", list(df.columns))

        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def clean_data(df):

    df = df.dropna()

    df = df.drop_duplicates()

    # normalizar columnas
    df.columns = df.columns.str.lower().str.strip()

    print("Columnas normalizadas:", list(df.columns))

    cantidad_col = None
    precio_col = None
    producto_col = None

    for col in df.columns:

        # detectar cantidad
        if col in ["cantidad", "cant", "qty", "quantity", "units"]:
            cantidad_col = col

        # detectar precio
        if col in ["precio", "price", "unit_price", "precio_unitario"]:
            precio_col = col

        # detectar producto
        if col in ["producto", "product", "item", "name"]:
            producto_col = col

    print("Cantidad column:", cantidad_col)
    print("Precio column:", precio_col)
    print("Producto column:", producto_col)

    if cantidad_col is None:
        raise Exception("No se encontró columna de cantidad")

    if precio_col is None:
        raise Exception("No se encontró columna de precio")

    df['total'] = df[cantidad_col] * df[precio_col]

    return df, producto_col


def create_summary(df, producto_col):

    if producto_col is None:

        summary = df[['total']].sum().to_frame(name="total").reset_index()

    else:

        summary = df.groupby(producto_col)['total'].sum().reset_index()

    return summary


def save_excel(df, summary):

    os.makedirs("output", exist_ok=True)

    with pd.ExcelWriter("output/reporte_final.xlsx") as writer:

        df.to_excel(writer, sheet_name="data", index=False)

        summary.to_excel(writer, sheet_name="summary", index=False)


def main():

    print("Excel Data Pipeline Started")

    folder = sys.argv[1]

    df = load_files(folder)

    df, producto_col = clean_data(df)

    summary = create_summary(df, producto_col)

    save_excel(df, summary)

    print("Excel Data Pipeline Finished Successfully")


if __name__ == "__main__":

    main()