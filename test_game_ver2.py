
import streamlit as st
import random

def initialize_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.guesses = []

def check_guess():
    guess = st.session_state.guess_input
    st.session_state.attempts += 1
    st.session_state.guesses.append(guess)
    
    if guess == st.session_state.secret_number:
        st.session_state.game_over = True
        st.balloons()
    elif st.session_state.attempts >= 5:
        st.session_state.game_over = True
    else:
        if guess < st.session_state.secret_number:
            st.session_state.last_hint = "⬆️ もっと大きい数字です！"
        else:
            st.session_state.last_hint = "⬇️ もっと小さい数字です！"

def main():
    st.title("🎮 数字当てゲーム")
    st.write("1から100までの数字を5回以内に当ててください！")

    if 'secret_number' not in st.session_state:
        initialize_game()

    # ゲーム状態の表示
    st.subheader(f"残り試行回数: {5 - st.session_state.attempts}")
    
    # 前回のヒント表示
    if hasattr(st.session_state, 'last_hint'):
        st.markdown(f"**ヒント**: {st.session_state.last_hint}")

    # 入力フォーム
    with st.form("guess_form"):
        guess = st.number_input(
            "数字を入力してください", 
            min_value=1, 
            max_value=100,
            key="guess_input"
        )
        submitted = st.form_submit_button("挑戦！", on_click=check_guess)

    # ゲームオーバー時の処理
    if st.session_state.game_over:
        if st.session_state.secret_number == st.session_state.guess_input:
            st.success(f"🎉 正解！ {st.session_state.secret_number}を{st.session_state.attempts}回目で当てました！")
        else:
            st.error(f"ゲームオーバー... 正解は {st.session_state.secret_number} でした！")
        
        if st.button("もう一度遊ぶ"):
            initialize_game()
            st.rerun()

    # これまでの予想履歴
    if st.session_state.guesses:
        st.subheader("予想履歴")
        for i, g in enumerate(st.session_state.guesses, 1):
            st.write(f"{i}回目: {g}")

if __name__ == "__main__":
    main()