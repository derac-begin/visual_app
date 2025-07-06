import streamlit as st
import pandas as pd
from datetime import datetime, time

def main():
    st.set_page_config(layout="wide") 
    st.title("時系列データ可視化アプリケーション")
    
    try:
        df = pd.read_csv(
            "sample.csv",
            index_col=0,
            parse_dates=True
        )
    except FileNotFoundError:
        st.error("エラー: 'data'フォルダに'sample.csv'ファイルが見つかりません。")
        return
    except Exception as e:
        st.error(f"データの読み込みまたは解析中にエラーが発生しました: {e}")
        return

    if df.empty:
        st.warning("データファイルが空です。")
        return

    if not isinstance(df.index, pd.DatetimeIndex):
        st.error("DataFrameのインデックスがDatetimeIndexではありません。CSVの解析を確認してください。")
        return

    st.sidebar.header("フィルターオプション")

    start_date_default = df.index.min().date()
    end_date_default = df.index.max().date()

    select_dates = st.sidebar.date_input(
        "日付範囲を選択してください:",
        value=(start_date_default, end_date_default),
        min_value=start_date_default,
        max_value=end_date_default,
        help="グラフに表示する日付の範囲を選択してください。"
    )

    if len(select_dates) == 2:
        start_datetime = datetime.combine(select_dates[0], time.min) 
        end_datetime = datetime.combine(select_dates[1], time.max) 

        filtered_df = df.loc[(df.index >= start_datetime) & (df.index <= end_datetime)]

        if filtered_df.empty:
            st.warning("選択された日付範囲にデータがありません。")
        else:
            plot_data = filtered_df.resample('D').mean()
            st.subheader("選択されたデータの折れ線グラフ (日次平均)")
            if not plot_data.empty:
                st.line_chart(plot_data)
                st.subheader("選択されたデータのプレビュー (日次平均)")
                st.dataframe(plot_data)
            else:
                st.info("選択された期間では、リサンプル後にプロットするデータがありません。")
    else:
        st.info("開始日と終了日を選択してください。")

if __name__ == "__main__":
    main()
