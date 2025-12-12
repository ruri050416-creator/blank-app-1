import streamlit as st
import random
import time
import pandas as pd


def generate_problem(categories=(1, 2, 3, 4, 5), total_items=16):
    items = [random.choice(categories) for _ in range(total_items)]
    counts = {c: items.count(c) for c in categories}
    # create a grid layout for display
    grid_rows = []
    cols_per_row = 4
    for i in range(0, len(items), cols_per_row):
        grid_rows.append(items[i : i + cols_per_row])
    return {
        "items": items,
        "grid": grid_rows,
        "counts": counts,
        "categories": list(categories),
        "total": total_items,
    }


def reset_user_inputs(problem):
    for c in problem["categories"]:
        st.session_state[f"input_{c}"] = 0


if "problem" not in st.session_state:
    st.session_state.problem = generate_problem()
    reset_user_inputs(st.session_state.problem)


st.title("📊 막대그래프 세우기 연습")
st.write("숫자들이 섞여 있어요. 각 숫자가 몇 개인지 세어서 아래에 입력하고 `제출`을 눌러보세요.")

with st.expander("문제 설명 (초등학생용)"):
    st.write(
        "1) 화면에 섞여 있는 숫자를 잘 세요. 2) 각 숫자 옆에 몇 개인지 입력하세요. 3) '제출'을 눌러 정답을 확인하고, 맞으면 다음 문제로 넘어가요."
    )

problem = st.session_state.problem

st.subheader("섞인 숫자들")
for row in problem["grid"]:
    cols = st.columns(len(row))
    for c, val in zip(cols, row):
        c.markdown(f"**{val}**", unsafe_allow_html=True)

st.markdown("---")

st.subheader("각 숫자의 개수를 입력하세요")
inputs = {}
cols = st.columns(len(problem["categories"]))
for i, cat in enumerate(problem["categories"]):
    key = f"input_{cat}"
    inputs[cat] = cols[i].number_input(
        label=str(cat), min_value=0, max_value=problem["total"], value=st.session_state.get(key, 0), key=key
    )

st.write("---")

st.subheader("내가 그린 막대그래프 (미리보기)")
df_user = pd.DataFrame({"category": list(inputs.keys()), "count": list(inputs.values())})
df_user = df_user.set_index("category")
st.bar_chart(df_user)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("제출"):
        correct = all(int(inputs[c]) == int(problem["counts"][c]) for c in problem["categories"])
        if correct:
            st.success("정답이에요! 🎉")
            st.info("넘어갑니다...")
            time.sleep(1.2)
            st.session_state.problem = generate_problem()
            reset_user_inputs(st.session_state.problem)
            st.experimental_rerun()
        else:
            st.error("아직 틀렸어요. 다시 확인해보세요.")
with col2:
    if st.button("정답 보기"):
        st.info("정답 (각 숫자별 개수)")
        st.write(problem["counts"])
        df_answer = pd.DataFrame({"category": list(problem["counts"].keys()), "count": list(problem["counts"].values())})
        df_answer = df_answer.set_index("category")
        st.bar_chart(df_answer)
with col3:
    if st.button("다음 문제"):
        st.info("넘어갑니다...")
        time.sleep(1.0)
        st.session_state.problem = generate_problem()
        reset_user_inputs(st.session_state.problem)
        st.experimental_rerun()

st.write("---")
st.caption("학습용 간단 앱 — 필요하면 기능 추가해드릴게요.")

