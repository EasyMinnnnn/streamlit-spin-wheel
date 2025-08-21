# app.py
import streamlit as st
import plotly.graph_objects as go
import random

st.title("Vòng quay may mắn")
names = st.text_area("Nhập danh sách tên, mỗi dòng một người:").strip().splitlines()

if names:
    if st.button("Quay số"):
        # tạo góc quay ngẫu nhiên
        start_angle = random.uniform(0, 360)
        # xác định người trúng
        selected_idx = int(((360 - start_angle) % 360) / (360 / len(names)))
        selected_name = names[selected_idx]
        st.write(f"🎉 Chúc mừng **{selected_name}**!")
        
        # vẽ biểu đồ vòng tròn
        fig = go.Figure(data=[go.Pie(labels=names,
                                     values=[1]*len(names),
                                     hole=0.3,
                                     rotation=start_angle,
                                     sort=False)])
        fig.update_layout(showlegend=False,
                          annotations=[dict(text="Quay", x=0.5, y=0.5, font_size=20, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Hãy nhập ít nhất một tên để bắt đầu.")
