import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
import base64

# Page configuration
st.set_page_config(
    page_title="성적 우수 장학금 관리 시스템",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'students_data' not in st.session_state:
    st.session_state.students_data = pd.DataFrame()
if 'scholarship_results' not in st.session_state:
    st.session_state.scholarship_results = pd.DataFrame()
if 'ranking_results' not in st.session_state:
    st.session_state.ranking_results = pd.DataFrame()
if 'quota_results' not in st.session_state:
    st.session_state.quota_results = {}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1e3c72;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="main-header">
    <h1>🎓 성적 우수 장학금 관리 시스템</h1>
    <p>Academic Excellence Scholarship Management System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📋 시스템 메뉴")
menu = st.sidebar.selectbox("기능 선택", [
    "🏠 홈",
    "👥 학생 데이터 관리", 
    "📊 성적 순위 산출", 
    "💰 예산 및 TO 관리", 
    "🏆 장학생 선정", 
    "📈 결과 보고서"
])

def create_download_link(df, filename, link_text):
    """Create a download link for dataframe"""
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:text/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def generate_sample_data():
    """Generate comprehensive sample student data"""
    np.random.seed(42)
    n_students = 150
    
    colleges = ['공과대학', '경영대학', '인문대학', '자연과학대학', '사회과학대학']
    departments = {
        '공과대학': ['컴퓨터공학과', '기계공학과', '전자공학과', '건축학과'],
        '경영대학': ['경영학과', '회계학과', '국제경영학과', '마케팅학과'],
        '인문대학': ['국어국문학과', '영어영문학과', '사학과', '철학과'],
        '자연과학대학': ['수학과', '물리학과', '화학과', '생물학과'],
        '사회과학대학': ['사회학과', '정치외교학과', '심리학과', '경제학과']
    }
    
    admission_types = ['일반전형', '학생부종합전형', '특별전형', '정시전형', '수시전형']
    admission_categories = ['신입학', '편입학', '재입학']
    
    data = []
    for i in range(n_students):
        college = np.random.choice(colleges)
        department = np.random.choice(departments[college])
        grade = np.random.choice([1, 2, 3, 4], p=[0.3, 0.3, 0.25, 0.15])
        
        # Generate realistic GPA based on grade (higher grades tend to have higher GPAs)
        base_gpa = 3.0 + (grade * 0.1) + np.random.normal(0, 0.4)
        
        student = {
            'student_id': f"202{grade}{i:04d}",
            'name': f"학생{i+1:03d}",
            'college': college,
            'department': department,
            'grade': grade,
            'student_type': '정규과정',
            'admission_type': np.random.choice(admission_types),
            'admission_category': np.random.choice(admission_categories, p=[0.8, 0.15, 0.05]),
            'prev_semester_gpa': np.clip(base_gpa, 0.0, 4.5),
            'prev_semester_credits': np.random.randint(15, 22),
            'prev_semester_major_credits': np.random.randint(6, 15),
            'academic_status': np.random.choice(['재학', '휴학', '제적'], p=[0.85, 0.12, 0.03]),
            'total_credits': grade * 35 + np.random.randint(-10, 20),
            'entrance_year': 2024 - grade + np.random.choice([-1, 0, 1], p=[0.1, 0.8, 0.1])
        }
        
        # Add some academic record changes
        if np.random.random() < 0.2:  # 20% chance of having academic changes
            student['academic_change_date'] = f"2023-{np.random.randint(3,12):02d}-{np.random.randint(1,28):02d}"
            student['academic_change_type'] = np.random.choice(['전과', '복수전공', '부전공'])
        else:
            student['academic_change_date'] = None
            student['academic_change_type'] = None
            
        data.append(student)
    
    return pd.DataFrame(data)

# Home Page
if menu == "🏠 홈":
    st.header("시스템 개요")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 📋 주요 기능
        
        **1. 학생 데이터 관리**
        - 정규과정 학부생 자격 검증
        - 기본 정보 및 입학 정보 관리
        - 학적 변동 이력 추적
        
        **2. 성적 순위 산출 (FUR-004)**
        - 직전 학기 평점평균 기준 순위 계산
        - 동점자 처리 (취득학점, 전공학점 순)
        - 학과별 순위 산정
        
        **3. 예산 및 TO 관리 (FUR-005)**
        - 부서별 장학 예산 입력 및 관리
        - 단과대학별 예산 배분
        - 장학금 종류별 TO 산출
        
        **4. 장학생 선정 (FUR-006)**
        - 순위와 TO를 결합한 대상자 선정
        - 장학 데이터 생성 및 배정
        - 자동 고지서 반영 준비
        """)
    
    with col2:
        st.markdown("""
        ### 📊 시스템 현황
        """)
        
        if not st.session_state.students_data.empty:
            st.metric("등록된 학생", len(st.session_state.students_data), "명")
            st.metric("단과대학", st.session_state.students_data['college'].nunique(), "개")
            
            if not st.session_state.scholarship_results.empty:
                st.metric("선정된 장학생", len(st.session_state.scholarship_results), "명")
            else:
                st.metric("선정된 장학생", 0, "명")
        else:
            st.info("아직 데이터가 없습니다.\n학생 데이터 관리에서 데이터를 입력해주세요.")
    
    # Quick start guide
    st.markdown("""
    ### 🚀 빠른 시작 가이드
    
    1. **학생 데이터 관리** → 샘플 데이터 생성 또는 CSV 파일 업로드
    2. **성적 순위 산출** → 자격 요건 설정 후 순위 계산 실행
    3. **예산 및 TO 관리** → 총 예산 및 장학금 금액 입력 후 TO 계산
    4. **장학생 선정** → 순위와 TO를 바탕으로 장학생 자동 선정
    5. **결과 보고서** → 최종 결과 확인 및 CSV 파일 다운로드
    """)

# Student Data Management
elif menu == "👥 학생 데이터 관리":
    st.header("📋 학생 데이터 관리")
    
    tab1, tab2, tab3 = st.tabs(["데이터 입력", "데이터 확인", "자격 요건 검증"])
    
    with tab1:
        st.subheader("데이터 입력 방식 선택")
        
        data_option = st.radio("입력 방식", ["🔄 샘플 데이터 생성", "📁 CSV 파일 업로드"])
        
        if data_option == "🔄 샘플 데이터 생성":
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if st.button("샘플 데이터 생성", type="primary"):
                    with st.spinner("데이터 생성 중..."):
                        st.session_state.students_data = generate_sample_data()
                    st.success("✅ 샘플 데이터 생성 완료!")
            
            with col2:
                st.info("🔍 샘플 데이터에는 150명의 학생 정보가 포함됩니다.")
        
        else:
            uploaded_file = st.file_uploader(
                "📁 학생 데이터 CSV 파일 업로드", 
                type=['csv'],
                help="CSV 파일은 UTF-8 인코딩이어야 합니다."
            )
            
            if uploaded_file is not None:
                try:
                    st.session_state.students_data = pd.read_csv(uploaded_file)
                    st.success(f"✅ 파일 업로드 완료! ({len(st.session_state.students_data)}명)")
                except Exception as e:
                    st.error(f"❌ 파일 읽기 오류: {str(e)}")
        
        # CSV 템플릿 다운로드
        if st.button("📥 CSV 템플릿 다운로드"):
            template_data = {
                'student_id': ['20211001', '20211002'],
                'name': ['홍길동', '김철수'],
                'college': ['공과대학', '경영대학'],
                'department': ['컴퓨터공학과', '경영학과'],
                'grade': [2, 3],
                'student_type': ['정규과정', '정규과정'],
                'admission_type': ['일반전형', '특별전형'],
                'admission_category': ['신입학', '신입학'],
                'prev_semester_gpa': [3.75, 3.42],
                'prev_semester_credits': [18, 19],
                'prev_semester_major_credits': [12, 9],
                'academic_status': ['재학', '재학']
            }
            template_df = pd.DataFrame(template_data)
            st.download_button(
                "CSV 템플릿 다운로드",
                template_df.to_csv(index=False, encoding='utf-8-sig'),
                "student_data_template.csv",
                "text/csv"
            )
    
    with tab2:
        if st.session_state.students_data.empty:
            st.warning("⚠️ 학생 데이터가 없습니다. 먼저 데이터를 입력해주세요.")
        else:
            st.subheader("📊 데이터 현황")
            
            # Summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("총 학생 수", len(st.session_state.students_data))
            with col2:
                st.metric("단과대학 수", st.session_state.students_data['college'].nunique())
            with col3:
                st.metric("학과 수", st.session_state.students_data['department'].nunique())
            with col4:
                avg_gpa = st.session_state.students_data['prev_semester_gpa'].mean()
                st.metric("평균 GPA", f"{avg_gpa:.2f}")
            with col5:
                active_students = len(st.session_state.students_data[
                    st.session_state.students_data['academic_status'] == '재학'
                ])
                st.metric("재학생 수", active_students)
            
            # College distribution
            st.subheader("단과대학별 분포")
            college_dist = st.session_state.students_data['college'].value_counts()
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.bar_chart(college_dist)
            with col2:
                st.dataframe(college_dist.reset_index())
            
            # Detailed data view
            st.subheader("상세 데이터")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                colleges = ['전체'] + list(st.session_state.students_data['college'].unique())
                selected_college = st.selectbox("단과대학 필터", colleges)
            with col2:
                grades = ['전체'] + list(sorted(st.session_state.students_data['grade'].unique()))
                selected_grade = st.selectbox("학년 필터", grades)
            with col3:
                statuses = ['전체'] + list(st.session_state.students_data['academic_status'].unique())
                selected_status = st.selectbox("학적상태 필터", statuses)
            
            # Apply filters
            filtered_data = st.session_state.students_data.copy()
            if selected_college != '전체':
                filtered_data = filtered_data[filtered_data['college'] == selected_college]
            if selected_grade != '전체':
                filtered_data = filtered_data[filtered_data['grade'] == selected_grade]
            if selected_status != '전체':
                filtered_data = filtered_data[filtered_data['academic_status'] == selected_status]
            
            st.dataframe(filtered_data, use_container_width=True)
            
            # Download filtered data
            if len(filtered_data) > 0:
                st.download_button(
                    "📥 필터된 데이터 다운로드",
                    filtered_data.to_csv(index=False, encoding='utf-8-sig'),
                    f"filtered_students_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )
    
    with tab3:
        if st.session_state.students_data.empty:
            st.warning("⚠️ 학생 데이터가 없습니다.")
        else:
            st.subheader("자격 요건 검증")
            
            # Eligibility criteria
            col1, col2 = st.columns(2)
            with col1:
                min_gpa = st.slider("최소 GPA 기준", 0.0, 4.5, 2.0, 0.1)
                min_credits = st.slider("최소 취득 학점", 0, 25, 12, 1)
            
            with col2:
                exclude_types = st.multiselect(
                    "제외할 학생 유형",
                    ['교환학생', '시간제학생', '방문학생'],
                    default=['교환학생', '시간제학생', '방문학생']
                )
                
                required_status = st.multiselect(
                    "허용할 학적 상태",
                    list(st.session_state.students_data['academic_status'].unique()),
                    default=['재학']
                )
            
            if st.button("자격 검증 실행", type="primary"):
                # Apply eligibility criteria
                eligible = st.session_state.students_data[
                    (st.session_state.students_data['prev_semester_gpa'] >= min_gpa) &
                    (st.session_state.students_data['prev_semester_credits'] >= min_credits) &
                    (st.session_state.students_data['academic_status'].isin(required_status)) &
                    (~st.session_state.students_data['admission_category'].isin(exclude_types))
                ].copy()
                
                ineligible = st.session_state.students_data[
                    ~st.session_state.students_data.index.isin(eligible.index)
                ]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"✅ 자격 충족: {len(eligible)}명")
                    if len(eligible) > 0:
                        st.dataframe(eligible[['student_id', 'name', 'college', 'department', 
                                            'grade', 'prev_semester_gpa', 'academic_status']])
                
                with col2:
                    st.error(f"❌ 자격 미달: {len(ineligible)}명")
                    if len(ineligible) > 0:
                        st.dataframe(ineligible[['student_id', 'name', 'college', 'department', 
                                               'grade', 'prev_semester_gpa', 'academic_status']])

# Ranking Calculation
elif menu == "📊 성적 순위 산출":
    st.header("📊 성적 순위 산출 (FUR-004)")
    
    if st.session_state.students_data.empty:
        st.warning("⚠️ 먼저 학생 데이터를 입력해주세요.")
    else:
        tab1, tab2 = st.tabs(["순위 계산", "결과 확인"])
        
        with tab1:
            st.subheader("자격 요건 설정")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                min_gpa = st.slider("최소 GPA 기준", 0.0, 4.5, 2.0, 0.1)
            with col2:
                min_credits = st.slider("최소 취득 학점", 0, 25, 12, 1)
            with col3:
                exclude_inactive = st.checkbox("휴학생/제적생 제외", value=True)
            
            if st.button("📊 순위 계산 실행", type="primary"):
                with st.spinner("순위 계산 중..."):
                    # Filter eligible students
                    eligible = st.session_state.students_data.copy()
                    
                    # Apply filters
                    eligible = eligible[
                        (eligible['prev_semester_gpa'] >= min_gpa) &
                        (eligible['prev_semester_credits'] >= min_credits)
                    ]
                    
                    if exclude_inactive:
                        eligible = eligible[eligible['academic_status'] == '재학']
                    
                    if len(eligible) == 0:
                        st.error("❌ 자격 요건을 만족하는 학생이 없습니다.")
                    else:
                        # Calculate rankings by department and grade
                        ranking_results = []
                        
                        for (dept, grade), group in eligible.groupby(['department', 'grade']):
                            sorted_group = group.sort_values([
                                'prev_semester_gpa',
                                'prev_semester_credits',
                                'prev_semester_major_credits'
                            ], ascending=[False, False, False]).copy()
                            
                            sorted_group['rank'] = range(1, len(sorted_group) + 1)
                            sorted_group['dept_grade'] = f"{dept}-{grade}학년"
                            ranking_results.append(sorted_group)
                        
                        st.session_state.ranking_results = pd.concat(ranking_results, ignore_index=True)
                        
                        st.success(f"✅ 순위 계산 완료! 총 {len(st.session_state.ranking_results)}명 대상")
                        
                        # Show summary by department
                        summary = st.session_state.ranking_results.groupby(['college', 'department', 'grade']).size().reset_index(name='student_count')
                        st.subheader("학과별 대상자 현황")
                        st.dataframe(summary, use_container_width=True)
        
        with tab2:
            if st.session_state.ranking_results.empty:
                st.info("먼저 순위 계산을 실행해주세요.")
            else:
                st.subheader("순위 계산 결과")
                
                # Filter options
                col1, col2, col3 = st.columns(3)
                with col1:
                    colleges = ['전체'] + list(st.session_state.ranking_results['college'].unique())
                    filter_college = st.selectbox("단과대학", colleges)
                with col2:
                    if filter_college != '전체':
                        departments = ['전체'] + list(st.session_state.ranking_results[
                            st.session_state.ranking_results['college'] == filter_college]['department'].unique())
                    else:
                        departments = ['전체'] + list(st.session_state.ranking_results['department'].unique())
                    filter_dept = st.selectbox("학과", departments)
                with col3:
                    grades = ['전체'] + list(sorted(st.session_state.ranking_results['grade'].unique()))
                    filter_grade = st.selectbox("학년", grades)
                
                # Apply filters
                filtered_rankings = st.session_state.ranking_results.copy()
                if filter_college != '전체':
                    filtered_rankings = filtered_rankings[filtered_rankings['college'] == filter_college]
                if filter_dept != '전체':
                    filtered_rankings = filtered_rankings[filtered_rankings['department'] == filter_dept]
                if filter_grade != '전체':
                    filtered_rankings = filtered_rankings[filtered_rankings['grade'] == filter_grade]
                
                # Display results
                display_cols = ['rank', 'student_id', 'name', 'college', 'department', 'grade',
                               'prev_semester_gpa', 'prev_semester_credits', 'prev_semester_major_credits']
                
                st.dataframe(filtered_rankings[display_cols].sort_values(['college', 'department', 'grade', 'rank']), 
                           use_container_width=True)
                
                # Download rankings
                st.download_button(
                    "📥 순위 결과 다운로드",
                    filtered_rankings.to_csv(index=False, encoding='utf-8-sig'),
                    f"ranking_results_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )

# Budget and Quota Management
elif menu == "💰 예산 및 TO 관리":
    st.header("💰 성적 우수 장학 TO 산출 (FUR-005)")
    
    if st.session_state.students_data.empty:
        st.warning("⚠️ 먼저 학생 데이터를 입력해주세요.")
    else:
        tab1, tab2 = st.tabs(["예산 설정", "TO 계산 결과"])
        
        with tab1:
            st.subheader("📊 예산 입력")
            
            col1, col2 = st.columns(2)
            with col1:
                total_budget = st.number_input(
                    "총 장학 예산 (원)", 
                    min_value=0, 
                    value=500000000, 
                    step=10000000,
                    format="%d"
                )
                st.write(f"입력 예산: {total_budget:,}원")
            
            with col2:
                semester = st.selectbox("적용 학기", ["1학기", "2학기", "연간"])
                budget_year = st.number_input("예산 연도", min_value=2020, max_value=2030, value=2024)
            
            st.subheader("🏆 장학금 종류별 금액 설정")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                yulgok_amount = st.number_input(
                    "율곡장학금 (원)", 
                    min_value=0, 
                    value=5000000, 
                    step=100000,
                    help="최우수 학생 대상"
                )
            with col2:
                dasan_amount = st.number_input(
                    "다산장학금 (원)", 
                    min_value=0, 
                    value=3000000, 
                    step=100000,
                    help="우수 학생 대상"
                )
            with col3:
                woncheon_amount = st.number_input(
                    "원천장학금 (원)", 
                    min_value=0, 
                    value=2000000, 
                    step=100000,
                    help="양호 학생 대상"
                )
            
            if st.button("💰 TO 계산 실행", type="primary"):
                with st.spinner("TO 계산 중..."):
                    # Calculate college-wise enrollment
                    college_enrollment = st.session_state.students_data[
                        st.session_state.students_data['academic_status'] == '재학'
                    ].groupby('college').size()
                    total_enrollment = college_enrollment.sum()
                    
                    # Calculate budget allocation
                    budget_allocation = {}
                    scholarship_amounts = {
                        '율곡장학': yulgok_amount,
                        '다산장학': dasan_amount,
                        '원천장학': woncheon_amount
                    }
                    
                    for college, count in college_enrollment.items():
                        ratio = count / total_enrollment
                        allocated_budget = total_budget * ratio
                        
                        # Calculate quotas for each scholarship type
                        quotas = {}
                        remaining_budget = allocated_budget
                        
                        # Prioritize quota allocation
                        for scholarship_type, amount in scholarship_amounts.items():
                            if remaining_budget >= amount:
                                base_quota = max(1, int(remaining_budget * 0.3 / amount))
                                quotas[scholarship_type] = base_quota
                                remaining_budget -= base_quota * amount
                            else:
                                quotas[scholarship_type] = 1  # Minimum allocation
                        
                        budget_allocation[college] = {
                            'enrollment': count,
                            'ratio': ratio,
                            'budget': allocated_budget,
                            'quotas': quotas
                        }
                    
                    st.session_state.quota_results = budget_allocation
                    st.success("✅ TO 계산이 완료되었습니다!")
        
        with tab2:
            if not st.session_state.quota_results:
                st.info("먼저 TO 계산을 실행해주세요.")
            else:
                st.subheader("📋 단과대학별 예산 배정 결과")
                
                # Create budget summary table
                budget_summary = []
                total_quotas = {'율곡장학': 0, '다산장학': 0, '원천장학': 0}
                
                for college, data in st.session_state.quota_results.items():
                    row = {
                        '단과대학': college,
                        '재학생수': data['enrollment'],
                        '비율': f"{data['ratio']:.1%}",
                        '배정예산': f"{data['budget']:,.0f}원",
                        '율곡장학TO': data['quotas']['율곡장학'],
                        '다산장학TO': data['quotas']['다산장학'],
                        '원천장학TO': data['quotas']['원천장학'],
                        '총TO': sum(data['quotas'].values())
                    }
                    budget_summary.append(row)
                    
                    for scholarship_type in total_quotas:
                        total_quotas[scholarship_type] += data['quotas'][scholarship_type]
                
                budget_df = pd.DataFrame(budget_summary)
                st.dataframe(budget_df, use_container_width=True)
                
                # Summary metrics
                st.subheader("📊 전체 TO 현황")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("율곡장학 TO", total_quotas['율곡장학'])
                with col2:
                    st.metric("다산장학 TO", total_quotas['다산장학'])
                with col3:
                    st.metric("원천장학 TO", total_quotas['원천장학'])
                with col4:
                    total_to = sum(total_quotas.values())
                    st.metric("전체 TO", total_to)
                
                # Detailed breakdown by department
                if st.checkbox("학과별 상세 TO 보기"):
                    st.subheader("학과별 상세 TO 배정")
                    
                    dept_details = []
                    for college, college_data in st.session_state.quota_results.items():
                        college_students = st.session_state.students_data[
                            (st.session_state.students_data['college'] == college) &
                            (st.session_state.students_data['academic_status'] == '재학')
                        ]
                        
                        dept_enrollment = college_students.groupby('department').size()
                        college_total = dept_enrollment.sum()
                        
                        for dept, count in dept_enrollment.items():
                            dept_ratio = count / college_total if college_total > 0 else 0
                            
                            # Distribute college quotas to departments
                            dept_quotas = {}
                            for scholarship_type, college_quota in college_data['quotas'].items():
                                dept_quota = max(1, int(college_quota * dept_ratio))
                                dept_quotas[scholarship_type] = dept_quota
                            
                            dept_details.append({
                                '단과대학': college,
                                '학과': dept,
                                '재학생수': count,
                                '율곡TO': dept_quotas['율곡장학'],
                                '다산TO': dept_quotas['다산장학'],
                                '원천TO': dept_quotas['원천장학'],
                                '계': sum(dept_quotas.values())
                            })
                    
                    dept_df = pd.DataFrame(dept_details)
                    st.dataframe(dept_df, use_container_width=True)
                
                # Download results
                st.download_button(
                    "📥 TO 결과 다운로드",
                    budget_df.to_csv(index=False, encoding='utf-8-sig'),
                    f"quota_results_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )

# Scholarship Assignment
elif menu == "🏆 장학생 선정":
    st.header("🏆 성적 우수 장학 대상자 선정 (FUR-006)")
    
    if st.session_state.ranking_results.empty or not st.session_state.quota_results:
        st.warning("⚠️ 먼저 순위 산출과 TO 관리를 완료해주세요.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.ranking_results.empty:
                st.error("❌ 순위 계산 미완료")
            else:
                st.success("✅ 순위 계산 완료")
        
        with col2:
            if not st.session_state.quota_results:
                st.error("❌ TO 계산 미완료")
            else:
                st.success("✅ TO 계산 완료")
                
    else:
        tab1, tab2 = st.tabs(["장학생 선정", "선정 결과"])
        
        with tab1:
            st.subheader("선정 조건 설정")
            
            col1, col2 = st.columns(2)
            with col1:
                selection_method = st.radio(
                    "선정 방식",
                    ["자동 선정 (순위 기준)", "수동 조정 가능"]
                )
            
            with col2:
                allow_duplicate = st.checkbox("중복 장학 허용", value=False)
                min_students_per_dept = st.number_input("학과별 최소 선정 인원", min_value=0, value=1)
            
            # Preview selection criteria
            st.info(f"""
            📋 **선정 기준 요약:**
            - 선정 방식: {selection_method}
            - 중복 장학: {'허용' if allow_duplicate else '불허'}
            - 학과별 최소 인원: {min_students_per_dept}명
            """)
            
            if st.button("🏆 장학생 선정 실행", type="primary"):
                with st.spinner("장학생 선정 중..."):
                    ranking_data = st.session_state.ranking_results
                    quota_data = st.session_state.quota_results
                    
                    scholarship_assignments = []
                    
                    # Assignment by college and department
                    for college in ranking_data['college'].unique():
                        college_data = ranking_data[ranking_data['college'] == college]
                        
                        if college in quota_data:
                            college_quotas = quota_data[college]['quotas']
                            
                            # Get departments in this college
                            departments = college_data['department'].unique()
                            
                            for dept in departments:
                                dept_data = college_data[college_data['department'] == dept]
                                
                                # Sort by rank within department
                                for grade in sorted(dept_data['grade'].unique()):
                                    grade_data = dept_data[dept_data['grade'] == grade]
                                    sorted_students = grade_data.sort_values('rank')
                                    
                                    # Assign scholarships based on quotas
                                    scholarship_types = ['율곡장학', '다산장학', '원천장학']
                                    assigned_count = 0
                                    
                                    # Calculate available slots for this dept-grade combination
                                    dept_enrollment = len(grade_data)
                                    total_college_enrollment = len(college_data)
                                    dept_ratio = dept_enrollment / total_college_enrollment if total_college_enrollment > 0 else 0
                                    
                                    available_slots = {}
                                    for scholarship_type, quota in college_quotas.items():
                                        slots = max(min_students_per_dept, int(quota * dept_ratio))
                                        available_slots[scholarship_type] = slots
                                    
                                    total_slots = sum(available_slots.values())
                                    
                                    # Assign scholarships to top students
                                    for i, (_, student) in enumerate(sorted_students.iterrows()):
                                        if assigned_count < total_slots and assigned_count < len(sorted_students):
                                            # Determine scholarship type based on rank
                                            if assigned_count < available_slots.get('율곡장학', 0):
                                                scholarship_type = '율곡장학'
                                                amount = 5000000  # This should come from settings
                                            elif assigned_count < available_slots.get('율곡장학', 0) + available_slots.get('다산장학', 0):
                                                scholarship_type = '다산장학'
                                                amount = 3000000
                                            else:
                                                scholarship_type = '원천장학'
                                                amount = 2000000
                                            
                                            assignment = student.copy()
                                            assignment['scholarship_type'] = scholarship_type
                                            assignment['scholarship_amount'] = amount
                                            assignment['assignment_date'] = datetime.now().strftime('%Y-%m-%d')
                                            assignment['assignment_semester'] = "2024-1"
                                            
                                            scholarship_assignments.append(assignment)
                                            assigned_count += 1
                    
                    if scholarship_assignments:
                        st.session_state.scholarship_results = pd.DataFrame(scholarship_assignments)
                        st.success(f"✅ 장학생 선정 완료! 총 {len(scholarship_assignments)}명 선정")
                        
                        # Show summary
                        summary_by_type = st.session_state.scholarship_results['scholarship_type'].value_counts()
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("율곡장학", summary_by_type.get('율곡장학', 0))
                        with col2:
                            st.metric("다산장학", summary_by_type.get('다산장학', 0))
                        with col3:
                            st.metric("원천장학", summary_by_type.get('원천장학', 0))
                    else:
                        st.error("❌ 선정된 장학생이 없습니다. 조건을 확인해주세요.")
        
        with tab2:
            if st.session_state.scholarship_results.empty:
                st.info("먼저 장학생 선정을 실행해주세요.")
            else:
                st.subheader("🎉 장학생 선정 결과")
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("총 선정자", len(st.session_state.scholarship_results))
                
                with col2:
                    total_amount = st.session_state.scholarship_results['scholarship_amount'].sum()
                    st.metric("총 장학금", f"{total_amount:,}원")
                
                with col3:
                    colleges_count = st.session_state.scholarship_results['college'].nunique()
                    st.metric("참여 단과대학", f"{colleges_count}개")
                
                with col4:
                    avg_gpa = st.session_state.scholarship_results['prev_semester_gpa'].mean()
                    st.metric("평균 GPA", f"{avg_gpa:.2f}")
                
                # Detailed results by scholarship type
                st.subheader("장학 종류별 현황")
                scholarship_summary = st.session_state.scholarship_results.groupby(['college', 'scholarship_type']).agg({
                    'student_id': 'count',
                    'scholarship_amount': 'sum'
                }).reset_index()
                scholarship_summary.columns = ['단과대학', '장학종류', '선정인원', '총장학금']
                scholarship_summary['총장학금'] = scholarship_summary['총장학금'].apply(lambda x: f"{x:,}원")
                
                pivot_summary = scholarship_summary.pivot_table(
                    index='단과대학', 
                    columns='장학종류', 
                    values='선정인원', 
                    fill_value=0
                )
                st.dataframe(pivot_summary, use_container_width=True)
                
                # Detailed student list
                st.subheader("선정자 명단")
                
                # Filters for detailed view
                col1, col2, col3 = st.columns(3)
                with col1:
                    filter_college = st.selectbox(
                        "단과대학 필터", 
                        ['전체'] + list(st.session_state.scholarship_results['college'].unique())
                    )
                with col2:
                    filter_scholarship = st.selectbox(
                        "장학 종류 필터",
                        ['전체'] + list(st.session_state.scholarship_results['scholarship_type'].unique())
                    )
                with col3:
                    sort_by = st.selectbox(
                        "정렬 기준",
                        ['순위순', 'GPA순', '학과순', '학번순']
                    )
                
                # Apply filters
                filtered_results = st.session_state.scholarship_results.copy()
                if filter_college != '전체':
                    filtered_results = filtered_results[filtered_results['college'] == filter_college]
                if filter_scholarship != '전체':
                    filtered_results = filtered_results[filtered_results['scholarship_type'] == filter_scholarship]
                
                # Apply sorting
                if sort_by == '순위순':
                    filtered_results = filtered_results.sort_values(['college', 'department', 'grade', 'rank'])
                elif sort_by == 'GPA순':
                    filtered_results = filtered_results.sort_values('prev_semester_gpa', ascending=False)
                elif sort_by == '학과순':
                    filtered_results = filtered_results.sort_values(['college', 'department', 'name'])
                else:  # 학번순
                    filtered_results = filtered_results.sort_values('student_id')
                
                # Display results
                display_columns = [
                    'rank', 'student_id', 'name', 'college', 'department', 'grade',
                    'prev_semester_gpa', 'scholarship_type', 'scholarship_amount', 'assignment_date'
                ]
                
                # Format amount column for display
                display_df = filtered_results[display_columns].copy()
                display_df['scholarship_amount'] = display_df['scholarship_amount'].apply(lambda x: f"{x:,}원")
                
                st.dataframe(display_df, use_container_width=True)
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 선정자 명단 다운로드",
                        filtered_results.to_csv(index=False, encoding='utf-8-sig'),
                        f"scholarship_recipients_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )
                
                with col2:
                    # Create summary report
                    summary_report = scholarship_summary.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        "📊 요약 보고서 다운로드",
                        summary_report,
                        f"scholarship_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )

# Results Report
elif menu == "📈 결과 보고서":
    st.header("📈 최종 결과 보고서")
    
    if st.session_state.scholarship_results.empty:
        st.warning("⚠️ 먼저 장학생 선정을 완료해주세요.")
    else:
        tab1, tab2, tab3 = st.tabs(["📊 종합 현황", "📋 상세 분석", "📁 문서 출력"])
        
        with tab1:
            st.subheader("🎯 전체 현황 대시보드")
            
            # Top-level metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            results = st.session_state.scholarship_results
            
            with col1:
                st.metric("총 선정자", len(results), "명")
            with col2:
                total_budget = results['scholarship_amount'].sum()
                st.metric("집행 예산", f"{total_budget/100000000:.1f}억원")
            with col3:
                avg_gpa = results['prev_semester_gpa'].mean()
                st.metric("평균 GPA", f"{avg_gpa:.2f}")
            with col4:
                colleges = results['college'].nunique()
                st.metric("참여 대학", f"{colleges}개")
            with col5:
                departments = results['department'].nunique()
                st.metric("참여 학과", f"{departments}개")
            
            # Charts and visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("장학 종류별 분포")
                scholarship_dist = results['scholarship_type'].value_counts()
                st.bar_chart(scholarship_dist)
                
                # Add percentage
                for scholarship, count in scholarship_dist.items():
                    percentage = count / len(results) * 100
                    st.write(f"• {scholarship}: {count}명 ({percentage:.1f}%)")
            
            with col2:
                st.subheader("단과대학별 선정 현황")
                college_dist = results['college'].value_counts()
                st.bar_chart(college_dist)
                
                # Show budget by college
                college_budget = results.groupby('college')['scholarship_amount'].sum()
                st.write("**예산 현황:**")
                for college, budget in college_budget.items():
                    st.write(f"• {college}: {budget:,}원")
            
            # Grade distribution
            st.subheader("학년별 선정 분포")
            grade_scholar = results.groupby(['grade', 'scholarship_type']).size().unstack(fill_value=0)
            st.bar_chart(grade_scholar)
            
            # GPA distribution
            st.subheader("선정자 GPA 분포")
            gpa_bins = pd.cut(results['prev_semester_gpa'], bins=[0, 3.0, 3.5, 4.0, 4.5], labels=['3.0미만', '3.0-3.5', '3.5-4.0', '4.0이상'])
            gpa_dist = gpa_bins.value_counts()
            st.bar_chart(gpa_dist)
        
        with tab2:
            st.subheader("📊 상세 분석")
            
            # Department-level analysis
            st.subheader("학과별 상세 현황")
            
            dept_analysis = results.groupby(['college', 'department']).agg({
                'student_id': 'count',
                'scholarship_amount': ['sum', 'mean'],
                'prev_semester_gpa': ['mean', 'min', 'max'],
                'rank': 'mean'
            }).round(2)
            
            dept_analysis.columns = ['선정인원', '총장학금', '평균장학금', '평균GPA', '최저GPA', '최고GPA', '평균순위']
            dept_analysis = dept_analysis.reset_index()
            
            # Format currency columns
            for col in ['총장학금', '평균장학금']:
                dept_analysis[col] = dept_analysis[col].apply(lambda x: f"{x:,.0f}원")
            
            st.dataframe(dept_analysis, use_container_width=True)
            
            # Correlation analysis
            st.subheader("성과 지표 상관관계")
            
            numeric_cols = ['prev_semester_gpa', 'prev_semester_credits', 'prev_semester_major_credits', 'rank', 'scholarship_amount']
            correlation_data = results[numeric_cols].copy()
            correlation_matrix = correlation_data.corr()
            
            st.write("**주요 상관관계:**")
            st.write("- GPA와 순위:", f"{correlation_matrix.loc['prev_semester_gpa', 'rank']:.3f}")
            st.write("- GPA와 장학금액:", f"{correlation_matrix.loc['prev_semester_gpa', 'scholarship_amount']:.3f}")
            st.write("- 취득학점과 GPA:", f"{correlation_matrix.loc['prev_semester_credits', 'prev_semester_gpa']:.3f}")
            
            # Top performers
            st.subheader("🏆 최우수 선정자 (상위 10명)")
            top_performers = results.nlargest(10, 'prev_semester_gpa')[
                ['student_id', 'name', 'college', 'department', 'grade', 'prev_semester_gpa', 'scholarship_type', 'scholarship_amount']
            ].copy()
            top_performers['scholarship_amount'] = top_performers['scholarship_amount'].apply(lambda x: f"{x:,}원")
            st.dataframe(top_performers, use_container_width=True)
            
            # Statistics by scholarship type
            st.subheader("장학 종류별 통계")
            
            scholarship_stats = results.groupby('scholarship_type').agg({
                'prev_semester_gpa': ['count', 'mean', 'std', 'min', 'max'],
                'scholarship_amount': 'sum'
            }).round(3)
            
            scholarship_stats.columns = ['인원', '평균GPA', 'GPA표준편차', '최저GPA', '최고GPA', '총예산']
            scholarship_stats = scholarship_stats.reset_index()
            scholarship_stats['총예산'] = scholarship_stats['총예산'].apply(lambda x: f"{x:,}원")
            
            st.dataframe(scholarship_stats, use_container_width=True)
        
        with tab3:
            st.subheader("📄 공식 문서 생성")
            
            # Generate comprehensive report
            st.subheader("보고서 생성 옵션")
            
            col1, col2 = st.columns(2)
            with col1:
                report_type = st.selectbox("보고서 유형", [
                    "전체 종합 보고서",
                    "단과대학별 보고서", 
                    "장학 종류별 보고서",
                    "학과별 상세 보고서"
                ])
            
            with col2:
                include_charts = st.checkbox("차트 포함", value=True)
                include_individual = st.checkbox("개별 학생 명단 포함", value=True)
            
            # Report generation
            if st.button("📄 보고서 생성", type="primary"):
                report_data = []
                
                # Header
                report_data.append("=" * 60)
                report_data.append("성적 우수 장학금 선정 결과 보고서")
                report_data.append(f"생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H시 %M분')}")
                report_data.append("=" * 60)
                report_data.append("")
                
                # Summary
                report_data.append("📊 전체 현황")
                report_data.append("-" * 30)
                report_data.append(f"• 총 선정 인원: {len(results):,}명")
                report_data.append(f"• 총 장학 예산: {results['scholarship_amount'].sum():,}원")
                report_data.append(f"• 참여 단과대학: {results['college'].nunique()}개")
                report_data.append(f"• 참여 학과: {results['department'].nunique()}개")
                report_data.append(f"• 평균 GPA: {results['prev_semester_gpa'].mean():.2f}")
                report_data.append("")
                
                # Scholarship type breakdown
                report_data.append("🏆 장학 종류별 현황")
                report_data.append("-" * 30)
                for scholarship_type in results['scholarship_type'].unique():
                    type_data = results[results['scholarship_type'] == scholarship_type]
                    report_data.append(f"• {scholarship_type}")
                    report_data.append(f"  - 선정 인원: {len(type_data)}명")
                    report_data.append(f"  - 총 예산: {type_data['scholarship_amount'].sum():,}원")
                    report_data.append(f"  - 평균 GPA: {type_data['prev_semester_gpa'].mean():.2f}")
                report_data.append("")
                
                # College breakdown
                report_data.append("🏫 단과대학별 현황")
                report_data.append("-" * 30)
                for college in sorted(results['college'].unique()):
                    college_data = results[results['college'] == college]
                    report_data.append(f"• {college}")
                    report_data.append(f"  - 선정 인원: {len(college_data)}명")
                    report_data.append(f"  - 총 예산: {college_data['scholarship_amount'].sum():,}원")
                    
                    # Scholarship type distribution within college
                    college_dist = college_data['scholarship_type'].value_counts()
                    for scholarship_type, count in college_dist.items():
                        report_data.append(f"    └ {scholarship_type}: {count}명")
                report_data.append("")
                
                # Individual list if requested
                if include_individual:
                    report_data.append("👥 선정자 명단")
                    report_data.append("-" * 30)
                    
                    for college in sorted(results['college'].unique()):
                        college_data = results[results['college'] == college].sort_values(['department', 'grade', 'rank'])
                        report_data.append(f"\n[{college}]")
                        
                        for _, student in college_data.iterrows():
                            report_data.append(
                                f"• {student['student_id']} {student['name']} "
                                f"({student['department']} {student['grade']}학년) - "
                                f"{student['scholarship_type']} (GPA: {student['prev_semester_gpa']:.2f})"
                            )
                
                report_text = "\n".join(report_data)
                
                # Display report
                st.text_area("생성된 보고서", report_text, height=400)
                
                # Download report
                st.download_button(
                    "📥 보고서 텍스트 다운로드",
                    report_text,
                    f"scholarship_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    "text/plain"
                )
            
            # Individual downloads
            st.subheader("개별 데이터 다운로드")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    "📋 전체 선정자 명단",
                    results.to_csv(index=False, encoding='utf-8-sig'),
                    f"all_recipients_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )
            
            with col2:
                summary_data = results.groupby(['college', 'scholarship_type']).agg({
                    'student_id': 'count',
                    'scholarship_amount': 'sum'
                }).reset_index()
                summary_data.columns = ['단과대학', '장학종류', '선정인원', '총장학금']
                
                st.download_button(
                    "📊 요약 통계",
                    summary_data.to_csv(index=False, encoding='utf-8-sig'),
                    f"summary_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )
            
            with col3:
                # Create detailed analytics
                detailed_analytics = results.groupby(['college', 'department', 'scholarship_type']).agg({
                    'student_id': 'count',
                    'scholarship_amount': ['sum', 'mean'],
                    'prev_semester_gpa': ['mean', 'min', 'max']
                }).round(2)
                
                detailed_analytics.columns = ['선정인원', '총장학금', '평균장학금', '평균GPA', '최저GPA', '최고GPA']
                detailed_analytics = detailed_analytics.reset_index()
                
                st.download_button(
                    "📈 상세 분석",
                    detailed_analytics.to_csv(index=False, encoding='utf-8-sig'),
                    f"detailed_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center;'>
<h4>📋 시스템 정보</h4>
<p><strong>성적 우수 장학금 관리 시스템</strong></p>
<p>Version 1.0</p>
<p>RFP: FUR-004/005/006</p>
</div>
""", unsafe_allow_html=True)

# Progress tracking in sidebar
st.sidebar.markdown("### 🔄 진행 상황")

progress_items = [
    ("학생 데이터", not st.session_state.students_data.empty),
    ("순위 계산", not st.session_state.ranking_results.empty), 
    ("TO 계산", bool(st.session_state.quota_results)),
    ("장학생 선정", not st.session_state.scholarship_results.empty)
]

for item_name, completed in progress_items:
    if completed:
        st.sidebar.markdown(f"✅ {item_name}")
    else:
        st.sidebar.markdown(f"⏳ {item_name}")

# Display current status
if not st.session_state.scholarship_results.empty:
    st.sidebar.success(f"🎉 시스템 완료!\n총 {len(st.session_state.scholarship_results)}명 선정")
