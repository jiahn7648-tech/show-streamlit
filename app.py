import streamlit as st

# 1. 초기 상태(Session State) 설정
# st.session_state는 앱의 상태를 저장하고 유지하는 데 사용됩니다.
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0 # 현재 온도의 초기값
if 'temp_A' not in st.session_state:
    st.session_state.temp_A = None # A 버튼에 저장된 온도 (초기에는 없음)
if 'temp_B' not in st.session_state:
    st.st.session_state.temp_B = None # B 버튼에 저장된 온도
if 'temp_C' not in st.session_state:
    st.session_state.temp_C = None # C 버튼에 저장된 온도

# 2. 버튼 클릭 시 동작할 함수 정의
def increment_temp():
    """온도를 1도 증가시킵니다."""
    st.session_state.temperature += 1

def decrement_temp():
    """온도를 1도 감소시킵니다."""
    st.session_state.temperature -= 1

def save_temp_to_slot(slot_name):
    """현재 온도를 지정된 슬롯에 저장하고, 저장된 슬롯을 표시합니다."""
    # 'last_saved_slot' 변수를 추가하여 어떤 슬롯에 저장할지 기억합니다.
    st.session_state.last_saved_slot = slot_name 

def recall_temp(slot_name):
    """지정된 슬롯에 저장된 온도를 현재 온도로 불러옵니다."""
    if st.session_state[f'temp_{slot_name}'] is not None:
        st.session_state.temperature = st.session_state[f'temp_{slot_name}']
    else:
        st.warning(f"경고: {slot_name} 버튼에 저장된 온도가 없습니다.")


# 3. Streamlit 앱 인터페이스 구성
st.title("🌡️ 온도 조절 및 저장 앱")

# 현재 온도 표시
# f-string을 사용하여 섭씨(℃)를 표시합니다.
st.markdown(f"## 현재 온도: **{st.session_state.temperature}°C**")

st.markdown("---")

# 온도 조절 버튼 (+ / -)
st.header("온도 조절")
col1, col2 = st.columns(2)
with col1:
    st.button("➕ 1°C 올리기", on_click=increment_temp)
with col2:
    st.button("➖ 1°C 내리기", on_click=decrement_temp)

st.markdown("---")

# 저장 기능: 먼저 '저장' 버튼을 누른 후, A, B, C 중 하나를 누릅니다.
st.header("온도 저장 및 불러오기")

# '저장' 버튼
if st.button("💾 저장", key="save_button"):
    st.session_state.is_saving = True # 저장 모드 활성화
    st.info("저장할 슬롯 (A, B, C)을 선택해 주세요.")

# 저장 슬롯 버튼 (A, B, C)
if st.session_state.get('is_saving', False):
    # 저장 모드일 때만 A, B, C 버튼이 '저장' 기능을 수행
    save_cols = st.columns(3)
    with save_cols[0]:
        if st.button("A 버튼 (저장)", key="save_A"):
            st.session_state.temp_A = st.session_state.temperature
            st.session_state.is_saving = False # 저장 모드 비활성화
            st.success(f"현재 온도 ({st.session_state.temperature}°C)가 A에 저장되었습니다.")
    with save_cols[1]:
        if st.button("B 버튼 (저장)", key="save_B"):
            st.session_state.temp_B = st.session_state.temperature
            st.session_state.is_saving = False
            st.success(f"현재 온도 ({st.session_state.temperature}°C)가 B에 저장되었습니다.")
    with save_cols[2]:
        if st.button("C 버튼 (저장)", key="save_C"):
            st.session_state.temp_C = st.session_state.temperature
            st.session_state.is_saving = False
            st.success(f"현재 온도 ({st.session_state.temperature}°C)가 C에 저장되었습니다.")
            
else:
    # 일반 모드일 때 (저장 모드가 아닐 때) A, B, C 버튼은 '불러오기' 기능을 수행
    recall_cols = st.columns(3)
    
    # A 버튼 불러오기
    with recall_cols[0]:
        label_A = f"A 불러오기 ({st.session_state.temp_A}°C)" if st.session_state.temp_A is not None else "A (저장된 온도 없음)"
        if st.button(label_A, on_click=recall_temp, args=['A'], key="recall_A"):
            if st.session_state.temp_A is not None:
                st.success(f"A에 저장된 온도 ({st.session_state.temp_A}°C)를 불러왔습니다.")

    # B 버튼 불러오기
    with recall_cols[1]:
        label_B = f"B 불러오기 ({st.session_state.temp_B}°C)" if st.session_state.temp_B is not None else "B (저장된 온도 없음)"
        if st.button(label_B, on_click=recall_temp, args=['B'], key="recall_B"):
            if st.session_state.temp_B is not None:
                st.success(f"B에 저장된 온도 ({st.session_state.temp_B}°C)를 불러왔습니다.")

    # C 버튼 불러오기
    with recall_cols[2]:
        label_C = f"C 불러오기 ({st.session_state.temp_C}°C)" if st.session_state.temp_C is not None else "C (저장된 온도 없음)"
        if st.button(label_C, on_click=recall_temp, args=['C'], key="recall_C"):
            if st.session_state.temp_C is not None:
                st.success(f"C에 저장된 온도 ({st.session_state.temp_C}°C)를 불러왔습니다.")

# 팁: 스트림릿은 버튼을 누를 때마다 코드를 처음부터 다시 실행합니다. 
# st.session_state를 사용하면 이전에 저장된 값을 유지할 수 있습니다.
