# ...existing code...
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
    # 위젯 생성 전에만 호출되어야 함
    for c in problem["categories"]:
        st.session_state[f"input_{c}"] = 0


# 초기화 로직: 문제가 없으면 문제 생성하고, 입력 리셋 플래그 설정
if "problem" not in st.session_state:
    st.session_state.problem = generate_problem()
    st.session_state.reset_inputs = True

# reset_inputs 키 보장
if "reset_inputs" not in st.session_state:
    st.session_state.reset_inputs = False

# 위젯 생성 전에 입력값 초기화 (플래그가 세워진 경우)
if st.session_state.reset_inputs:
    reset_user_inputs(st.session_state.problem)
    st.session_state.reset_inputs = False

# ...existing code...
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
# ...existing code...
with col1:
    if st.button("제출"):
        correct = all(int(inputs[c]) == int(problem["counts"][c]) for c in problem["categories"])
        if correct:
            st.success("정답이에요! 🎉")
            time.sleep(1.2)
            # 새 문제 생성 후, 직접 입력 리셋 대신 플래그 세우기 -> 위젯 생성 전에 초기화
            st.session_state.problem = generate_problem()
            st.session_state.reset_inputs = True
            # st.experimental_set_query_params -> st.query_params
            st.query_params = {"_rerun": [str(int(time.time() * 1000))]}
        else:
            st.error("아직 틀렸어요. 다시 확인해보세요.")
...
with col3:
    if st.button("다음 문제"):
        placeholder = st.empty()
        placeholder.info("넘어갑니다...")
        time.sleep(5.0)
        placeholder.empty()
        st.session_state.problem = generate_problem()
        st.session_state.reset_inputs = True
        # st.experimental_set_query_params -> st.query_params
        st.query_params = {"_rerun": [str(int(time.time() * 1000))]}
# ...existing code...

st.write("---")
st.caption("학습용 간단 앱 — 필요하면 기능 추가해드릴게요.")
# ...existing code...