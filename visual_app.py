import streamlit as st
import pandas as pd
from datetime import datetime, time # datetimeオブジェクトを扱うためにインポート

def main():
    st.set_page_config(layout="wide") # アプリのレイアウトを広めに設定
    st.title("時系列データ可視化アプリケーション") # アプリのタイトルを追加

    # --- データの読み込み ---
    try:
        # CSVファイルを読み込む。最初の列を日付として解析し、インデックスに設定。
        # parse_dates=True は、pandasに日付の解析を任せる最も簡単な方法です。
        df = pd.read_csv(
            "sample.csv",
            index_col=0, # 最初の列をインデックスに設定
            parse_dates=True # 日付として解析
        )
    except FileNotFoundError:
        st.error("エラー: 'data'フォルダに'sample.csv'ファイルが見つかりません。")
        return # ファイルがない場合は処理を終了
    except Exception as e:
        st.error(f"データの読み込みまたは解析中にエラーが発生しました: {e}")
        return

    if df.empty:
        st.warning("データファイルが空です。")
        return

    # インデックスがDatetimeIndexであることを確認
    if not isinstance(df.index, pd.DatetimeIndex):
        st.error("DataFrameのインデックスがDatetimeIndexではありません。CSVの解析を確認してください。")
        return

    # --- サイドバーにフィルターオプションを設定 ---
    st.sidebar.header("フィルターオプション")

    # デフォルトの選択範囲をデータ全体の最初と最後の日付部分に設定
    start_date_default = df.index.min().date()
    end_date_default = df.index.max().date()

    select_dates = st.sidebar.date_input(
        "日付範囲を選択してください:",
        value=(start_date_default, end_date_default),
        min_value=start_date_default,
        max_value=end_date_default,
        help="グラフに表示する日付の範囲を選択してください。"
    )

    # 日付が2つ選択されているか確認
    if len(select_dates) == 2:
        # st.date_inputから返されるのはdatetime.dateオブジェクトなので、
        # 時刻情報を持つdatetime.datetimeオブジェクトに変換して、日付範囲の完全な日を含めるようにする。
        start_datetime = datetime.combine(select_dates[0], time.min) # 選択された日の始まり
        end_datetime = datetime.combine(select_dates[1], time.max)   # 選択された日の終わり

        # --- データのフィルタリングとリサンプル ---
        # 選択された日付範囲でDataFrameをフィルタリング
        # .loc[]を使用することで、より明確に日付範囲でのスライスを示します。
        filtered_df = df.loc[(df.index >= start_datetime) & (df.index <= end_datetime)]

        if filtered_df.empty:
            st.warning("選択された日付範囲にデータがありません。")
        else:
            # データを日次平均にリサンプル
            # 動画では「電力使用量」のような単一の列をプロットしていると推測されます。
            # プロットしたい列名を指定するか、すべての数値列をプロットする場合は`filtered_df.resample('D').mean()`とします。
            # 例: plot_data = filtered_df[['電力使用量']].resample('D').mean()
            plot_data = filtered_df.resample('D').mean()


            # --- グラフの表示 ---
            st.subheader("選択されたデータの折れ線グラフ (日次平均)")
            if not plot_data.empty:
                st.line_chart(plot_data)

                # 選択された期間の生データ（日次平均）も表示 (オプション)
                st.subheader("選択されたデータのプレビュー (日次平均)")
                st.dataframe(plot_data)
            else:
                st.info("選択された期間では、リサンプル後にプロットするデータがありません。")
    else:
        st.info("開始日と終了日を選択してください。")

# スクリプトが直接実行された場合にmain関数を呼び出す
if __name__ == "__main__":
    main()
