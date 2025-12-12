import streamlit as st

# 1. 초기 상태(Session State) 설정
# 앱이 시작될 때 필요한 변수들을 st.session_state에 초기화합니다.
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0 # 현재 온도 (초기값: 0도)
if 'temp_A' not in st.session_state:
    st.session_state.temp_A = None # A 슬롯에 저장된 온도
if 'temp_B' not in st.session_state:
    st.session_state.temp_B = None # B 슬롯에 저장된 온도
if 'temp_C' not in st.session_state:
    st.session_state.temp_C = None # C 슬롯에 저장된 온도
if 'is_saving' not in st.session_state:
    st.session_state.is_saving = False # 저장 모드 활성화/비활성화 상태

# 2. 버튼 클릭 시 동작할 함수 정의
def increment_temp():
    """현재 온도를 1도 증가시킵니다."""
    st.session_state.temperature += 1
    # 저장 모드가 활성화되어 있다면, 온도 변경 시 저장 모드를 자동으로 해제 (선택 사항)
    st.session_state.is_saving = False 

def decrement_temp():
    """현재 온도를 1도 감소시킵니다."""
    st.session_state.temperature -= 1
    # 저장 모드가 활성화되어 있다면, 온도 변경 시 저장 모드를 자동으로 해제 (선택 사항)
    st.session_state.is_saving = False

def activate_save_mode():
    """저장 버튼을 눌렀을 때 호출되어 저장 모드를 활성화합니다."""
    st.session_state.is_saving = True
    
def save_temp_to_slot(slot_name):
    """현재 온도를 지정된 슬롯에 저장하고 저장 모드를 비활성화합니다."""
    
    # 딕셔너리 접근 방식으로 해당 슬롯에 현재 온도를 저장
    st.session_state[f'temp_{slot_name}'] = st.session_state.temperature
    
    # 저장 완료 후 저장 모드 비활성화
    st.session_state.is_saving = False 
    
    # 성공 메시지 표시 (Streamlit은 재실행되므로, 이 메시지는 잠시 보이고 사라집니다)
    # st.success(f"현재 온도 ({st.session_state.temperature}°C)가 {slot_name}에 저장되었습니다.")


def recall_temp(slot_name):
    """지정된 슬롯에 저장된 온도를 현재 온도로 불러옵니다."""
    
    # 저장된 온도가 None이 아닌지 확인
    saved_temp = st.session_state[f'temp_{slot_name}']
    
    if saved_temp is not None:
        st.session_state.temperature = saved_temp
        st.session_state.is_saving = False # 불러오기 시 저장 모드 비활성화
        # st.success(f"{slot_name}에 저장된 온도 ({saved_temp}°C)를 불러왔습니다.")
    else:
        st.warning(f"경고: {slot_name} 버튼에 저장된 온도가 없습니다.")


# 3. Streamlit 앱 인터페이스 구성
st.title("🌡️ 온도 조절 및 저장 앱")

# 현재 온도 표시
st.markdown(f"## 현재 온도: **{st.session_state.temperature}°C**")

st.markdown("---")

# --- 3-1. 온도 조절 버튼 (+ / -) ---
st.header("온도 조절")
col_plus, col_minus = st.columns(2)
with col_plus:
    st.button("➕ 1°C 올리기", on_click=increment_temp)
with col_minus:
    st.button("➖ 1°C 내리기", on_click=decrement_temp)

st.markdown("---")

# --- 3-2. 저장 및 불러오기 기능 ---
st.header("온도 저장 및 불러오기")

# '저장' 버튼 (저장 모드 활성화)
if st.button("💾 저장", key="activate_save", on_click=activate_save_mode):
    pass # on_click 핸들러에서 상태를 변경하므로, 이 블록에서는 별도의 동작이 필요 없습니다.

# 상태 메시지 표시
if st.session_state.is_saving:
    st.info("현재 온도를 저장할 슬롯 (A, B, C)을 **선택해 주세요.**")
else:
    st.info("A, B, C 버튼을 눌러 저장된 온도를 **불러올 수 있습니다.**")


# A, B, C 슬롯 버튼
slot_cols = st.columns(3)

# A 슬롯
with slot_cols[0]:
    if st.session_state.is_saving:
        # 저장 모드일 때 (저장 기능)
        st.button("A 버튼 (현재 온도 저장)", key="slot_A_save", 
                  on_click=save_temp_to_slot, args=['A'])
    else:
        # 일반 모드일 때 (불러오기 기능)
        label_A = f"A 불러오기 ({st.session_state.temp_A}°C)" if st.session_state.temp_A is not None else "A (저장된 온도 없음)"
        st.button(label_A, key="slot_A_recall", 
                  on_click=recall_temp, args=['A'])

# B 슬롯
with slot_cols[1]:
    if st.session_state.is_saving:
        # 저장 모드일 때 (저장 기능)
        st.button("B 버튼 (현재 온도 저장)", key="slot_B_save", 
                  on_click=save_temp_to_slot, args=['B'])
    else:
        # 일반 모드일 때 (불러오기 기능)
        label_B = f"B 불러오기 ({st.session_state.temp_B}°C)" if st.session_state.temp_B is not None else "B (저장된 온도 없음)"
        st.button(label_B, key="slot_B_recall", 
                  on_click=recall_temp, args=['B'])

# C 슬롯
with slot_cols[2]:
    if st.session_state.is_saving:
        # 저장 모드일 때 (저장 기능)
        st.button("C 버튼 (현재 온도 저장)", key="slot_C_save", 
                  on_click=save_temp_to_slot, args=['C'])
    else:
        # 일반 모드일 때 (불러오기 기능)
        label_C = f"C 불러오기 ({st.session_state.temp_C}°C)" if st.session_state.temp_C is not None else "C (저장된 온도 없음)"
        st.button(label_C, key="slot_C_recall", 
                  on_click=recall_temp, args=['C'])

st.markdown("---")
st.caption("팁: **💾 저장** 버튼을 누르면 A, B, C 버튼이 **저장** 기능으로 바뀝니다.")
