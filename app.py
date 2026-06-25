import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(
    page_title="AI & Automation Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================= CUSTOM CSS FOR COLORS (ĐỔI MÀU GIAO DIỆN) =================
st.markdown("""
    <style>
    /* 1. Đổi màu nền của Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f4f8;
        border-right: 2px solid #d1e3f0;
    }
    
    /* 2. Đổi màu Tiêu đề chính */
    .main-title {
        color: #1e3a8a; /* Màu xanh nước biển đậm đắt giá kiểu Corporate */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* 3. Tùy biến màu sắc và khung của các ô KPIs (Thẻ Metric) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border-left: 5px solid #3b82f6; /* Vạch màu xanh làm điểm nhấn bên trái giống Power BI */
    }
    
    /* Đổi màu chữ nhãn KPI (Label) */
    div[data-testid="stMetricLabel"] > div {
        color: #4a5568 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    
    /* Đổi màu trị số KPI (Value) */
    div[data-testid="stMetricValue"] > div {
        color: #1e3a8a !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HÀM ĐỌC DATA
@st.cache_data
def load_data():
    df1 = pd.read_csv(r"C:\Users\AD\OneDrive\Desktop\AI-Task-Visualization\data\raw\domain_worker_desires.csv")
    df2 = pd.read_csv(r"C:\Users\AD\OneDrive\Desktop\AI-Task-Visualization\data\raw\domain_worker_metadata.csv")
    df3 = pd.read_csv(r"C:\Users\AD\OneDrive\Desktop\AI-Task-Visualization\data\raw\expert_rated_technological_capability.csv")
    df4 = pd.read_csv(r"C:\Users\AD\OneDrive\Desktop\AI-Task-Visualization\data\raw\task_statement_with_metadata.csv")
    
    # Kết hợp dữ liệu Worker
    worker_full = pd.merge(df1, df2, on="User ID", suffixes=('', '_user'))
    worker_full = pd.merge(worker_full, df4, on="Task ID", suffixes=('', '_task'))
    
    # Kết hợp dữ liệu Expert
    expert_full = pd.merge(df3, df4, on="Task ID", suffixes=('', '_task'))
    
    # Tính toán ngầm bảng Friction (Xung đột) theo từng Task
    worker_avg = df1.groupby("Task ID")["Automation Desire Rating"].mean().reset_index()
    expert_avg = df3.groupby("Task ID")["Automation Capacity Rating"].mean().reset_index()
    
    friction_df = pd.merge(worker_avg, expert_avg, on="Task ID")
    friction_df["Friction Score"] = friction_df["Automation Desire Rating"] - friction_df["Automation Capacity Rating"]
    friction_df = pd.merge(friction_df, df4, on="Task ID")
    
    return worker_full, expert_full, friction_df

worker_df, expert_df, friction_df = load_data()

# 3. SIDEBAR VỚI TÍNH NĂNG CLEAR FILTER
st.sidebar.markdown("<h2 style='color: #1e3a8a; font-size: 1.5rem;'>⚙️ Bộ Lọc Thả Xuống</h2>", unsafe_allow_html=True)

# Tạo nút Clear Filter
if st.sidebar.button("🧹 Xóa bộ lọc (Reset)"):
    st.session_state["filter_occupation"] = "Tất cả"
    st.session_state["filter_exp"] = "Tất cả"
    st.session_state["filter_income"] = "Tất cả"

# Thiết lập giá trị mặc định trong session_state nếu chưa có
if "filter_occupation" not in st.session_state:
    st.session_state["filter_occupation"] = "Tất cả"
if "filter_exp" not in st.session_state:
    st.session_state["filter_exp"] = "Tất cả"
if "filter_income" not in st.session_state:
    st.session_state["filter_income"] = "Tất cả"

# Dropdown danh sách lọc sử dụng trạng thái session_state
all_occupations = ["Tất cả"] + list(worker_df["Occupation (O*NET-SOC Title)"].unique())
selected_occupation = st.sidebar.selectbox("1. Chọn Ngành Nghề:", all_occupations, key="filter_occupation")

all_exp = ["Tất cả"] + list(sorted(worker_df["Experience"].dropna().unique()))
selected_exp = st.sidebar.selectbox("2. Chọn Thâm Niên (Worker):", all_exp, key="filter_exp")

all_income = ["Tất cả"] + list(sorted(worker_df["Income"].dropna().unique()))
selected_income = st.sidebar.selectbox("3. Chọn Nhóm Thu Nhập (Worker):", all_income, key="filter_income")

# Áp dụng bộ lọc đồng bộ cho các bảng
filtered_worker = worker_df.copy()
filtered_expert = expert_df.copy()
filtered_friction = friction_df.copy()

if selected_occupation != "Tất cả":
    filtered_worker = filtered_worker[filtered_worker["Occupation (O*NET-SOC Title)"] == selected_occupation]
    filtered_expert = filtered_expert[filtered_expert["Occupation (O*NET-SOC Title)"] == selected_occupation]
    filtered_friction = filtered_friction[filtered_friction["Occupation (O*NET-SOC Title)"] == selected_occupation]

if selected_exp != "Tất cả":
    # Sửa từ filtered_exp thành ["Experience"]
    filtered_worker = filtered_worker[filtered_worker["Experience"] == selected_exp]

if selected_income != "Tất cả":
    # Sửa từ filtered_income thành ["Income"]
    filtered_worker = filtered_worker[filtered_worker["Income"] == selected_income]

# 4. TIÊU ĐỀ CHÍNH (Sử dụng class CSS đã định nghĩa ở trên)
st.markdown('<h1 class="main-title">📊 AI & Automation Tối Giản Dashboard</h1>', unsafe_allow_html=True)
st.write("---")

# 5. KHU VỰC KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric(label="Tổng số Task", value=f"{filtered_worker['Task ID'].nunique():,}")
with kpi2:
    avg_wage = filtered_worker["Occupation Mean Annual Wage"].mean()
    st.metric(label="Lương trung bình năm", value=f"${avg_wage:,.0f}" if not pd.isna(avg_wage) else "N/A")
with kpi3:
    st.metric(label="Điểm Worker muốn TĐH", value=f"{filtered_worker['Automation Desire Rating'].mean():.2f}")
with kpi4:
    st.metric(label="Chuyên gia chấm Khả năng", value=f"{filtered_expert['Automation Capacity Rating'].mean():.2f}")

st.write("---")

# 6. PHÂN CHIA TABS
tab1, tab2, tab3 = st.tabs(["🎯 So Sánh & Insight", "👥 Khảo Sát Worker", "🔍 Tra Cứu"])

# ================= TAB 1: SO SÁNH & INSIGHT ĐỘT PHÁ =================
with tab1:
    st.subheader("💡 Insight Đột Phá: Vùng Xung Đột Kỳ Vọng Tự Động Hóa")
    st.markdown("""
    *Những công việc có điểm **Xung đột cao nhất** là nơi Worker cực kỳ muốn tự động hóa (do áp lực/chán nản) nhưng Chuyên gia đánh giá công nghệ chưa sẵn sàng.*
    """)
    
    if not filtered_friction.empty:
        top_friction = filtered_friction.nlargest(5, "Friction Score")[["Task", "Friction Score", "Automation Desire Rating", "Automation Capacity Rating"]]
        top_friction.columns = ["Nội dung công việc (Task)", "Điểm Xung Đột", "Worker Muốn (1-5)", "Chuyên Gia Chấm (1-5)"]
        st.dataframe(top_friction, use_container_width=True, hide_index=True)
    else:
        st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại.")
    
    st.write("---")
    st.subheader("Biểu đồ phân tích rào cản & lý do")
    
    col1, col2 = st.columns(2)
    with col1:
        reasons_cols = [c for c in filtered_worker.columns if "Reasons for Automation Desire" in c]
        reasons_summary = filtered_worker[reasons_cols].sum().reset_index()
        reasons_summary.columns = ['Lý do', 'Số lượng']
        reasons_summary['Lý do'] = reasons_summary['Lý do'].str.replace("Reasons for Automation Desire - ", "")
        fig1 = px.bar(reasons_summary, x='Số lượng', y='Lý do', orientation='h', 
                      title="Lý do Worker muốn tự động hóa", 
                      color='Số lượng', color_continuous_scale='Blues')
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        expert_metrics = ['Physical Action Requirement', 'Involved Uncertainty', 'Domain Expertise Requirement', 'Interpersonal Communication Requirement']
        if not filtered_expert.empty:
            expert_avg = filtered_expert[expert_metrics].mean().reset_index()
            expert_avg.columns = ['Đặc tính', 'Điểm']
            fig2 = px.bar(expert_avg, x='Điểm', y='Đặc tính', orientation='h',
                          title="Yếu tố khiến Chuyên gia chấm điểm khó TĐH", 
                          color='Điểm', color_continuous_scale='Oranges')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("Không có dữ liệu chuyên gia cho bộ lọc này.")

# ================= TAB 2: KHẢO SÁT WORKER DEEP-DIVE =================
with tab2:
    st.subheader("Phân Tích Xu Hướng Người Lao Động")
    
    col3, col4 = st.columns(2)
    with col3:
        enjoyment_group = filtered_worker.groupby("Enjoyment Rating")["Automation Desire Rating"].mean().reset_index()
        fig3 = px.bar(enjoyment_group, x="Enjoyment Rating", y="Automation Desire Rating",
                      title="Điểm muốn TĐH trung bình theo Mức độ yêu thích công việc (1-5)",
                      color="Automation Desire Rating", color_continuous_scale='Greens')
        fig3.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))
        st.plotly_chart(fig3, use_container_width=True)
        
    with col4:
        fig4 = px.box(filtered_worker, x="LLM Familiarity", y="Automation Desire Rating",
                      title="Mức độ rành LLM vs Mong muốn TĐH", color="LLM Familiarity")
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

# ================= TAB 3: TRA CỨU CHI TIẾT =================
with tab3:
    st.subheader("Bảng tra cứu dữ liệu tổng hợp")
    display_df = filtered_worker[["Task ID", "Occupation (O*NET-SOC Title)", "Task", "Automation Desire Rating", "Enjoyment Rating"]].drop_duplicates()
    st.dataframe(display_df, use_container_width=True, hide_index=True)