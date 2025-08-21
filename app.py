import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Vòng quay may mắn", page_icon="🎲")

# Tiêu đề
st.title("Vòng quay may mắn 🎡")

# Nhập danh sách tên (mỗi dòng một người/một mục)
names_input = st.text_area(
    "Nhập danh sách tên hoặc lựa chọn (mỗi dòng một mục):"
).strip()
names = [n for n in names_input.splitlines() if n]

# Nếu có danh sách, hiển thị nút "Quay số"
if names:
    if st.button("Quay số"):
        # Tạo góc quay ngẫu nhiên
        start_angle = random.uniform(0, 360)
        # Xác định mục trúng thưởng dựa trên góc quay
        selected_idx = int(
            ((360 - start_angle) % 360) / (360 / len(names))
        )
        selected_name = names[selected_idx]

        # Hiển thị thông báo trúng thưởng
        st.success(f"🎉 Chúc mừng **{selected_name}**!")

        # Vẽ biểu đồ vòng tròn mô phỏng vòng quay
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=names,
                    values=[1] * len(names),
                    hole=0.3,
                    rotation=start_angle,
                    sort=False,
                )
            ]
        )
        fig.update_layout(
            showlegend=False,
            annotations=[
                dict(text="Quay", x=0.5, y=0.5, font_size=20, showarrow=False)
            ],
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Hãy nhập ít nhất một tên hoặc mục để bắt đầu.")

# --------- Tùy chọn: Vòng quay Chart.js (nhúng HTML/JS) ----------
# Nếu bạn muốn sử dụng Chart.js để có hiệu ứng quay mượt hơn,
# bỏ ghi chú phần bên dưới và cài thêm thư viện streamlit.components.v1:

# import streamlit.components.v1 as components
# import json
# if st.button("Quay bằng Chart.js"):
#     labels_json = json.dumps(names)
#     data_json = json.dumps([1] * len(names))
#     random_rotation = random.uniform(0, 360)
#     html_code = f"""
#     <canvas id="wheel"></canvas>
#     <button id="spin">Quay</button>
#     <p id="result"></p>
#     <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#     <script>
#       const labels = {labels_json};
#       const data = {{
#         labels: labels,
#         datasets: [{{
#           data: {data_json},
#           backgroundColor: labels.map((_, i) =>
#             `hsl(${{(i/labels.length)*360}}, 80%, 60%)`)
#         }}]
#       }};
#       const ctx = document.getElementById('wheel').getContext('2d');
#       const myChart = new Chart(ctx, {{
#         type: 'pie',
#         data: data,
#         options: {{
#           rotation: {random_rotation},
#           animation: {{
#             duration: 5000,
#             easing: 'easeOutCubic'
#           }},
#           plugins: {{
#             legend: {{ display: false }}
#           }}
#         }}
#       }});
#       document.getElementById('spin').onclick = function() {{
#         const randomAngle = Math.random() * 360;
#         myChart.options.rotation = randomAngle;
#         myChart.update();
#         const segmentSize = 360 / labels.length;
#         const idx = Math.floor(((360 - randomAngle) % 360) / segmentSize);
#         document.getElementById('result').innerHTML = 'Kết quả: ' + labels[idx];
#       }};
#     </script>
#     """
#     components.html(html_code, height=500)
