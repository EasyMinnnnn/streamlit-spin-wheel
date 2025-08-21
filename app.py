import streamlit as st
import streamlit.components.v1 as components
import json
import random

st.set_page_config(page_title="Vòng quay may mắn", page_icon="🎡")

st.title("🎡 Vòng quay may mắn có hiệu ứng & âm thanh")

# Nhập danh sách người chơi / mục tiêu
names_input = st.text_area("Nhập danh sách (mỗi dòng một tên):").strip()
names = [n for n in names_input.splitlines() if n]

# Đường dẫn file âm thanh (ví dụ: "click.mp3" để cùng repo)
sound_file = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"  

if names and st.button("Quay số 🎲"):
    labels = json.dumps(names)
    data_values = json.dumps([1] * len(names))

    html_code = f"""
    <canvas id="wheel" width="350" height="350"></canvas>
    <button id="spin" style="margin-top:10px;padding:10px 20px;font-size:16px;">Quay 🎡</button>
    <p id="result" style="font-size:20px;font-weight:bold;color:green;"></p>

    <audio id="tickSound" src="{sound_file}" preload="auto"></audio>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    const labels = {labels};
    const data = {{
      labels: labels,
      datasets: [{{
        data: {data_values},
        backgroundColor: labels.map((_, i) =>
          `hsl(${{(i/labels.length)*360}}, 80%, 60%)`)
      }}]
    }};
    const ctx = document.getElementById('wheel').getContext('2d');
    const myChart = new Chart(ctx, {{
      type: 'pie',
      data: data,
      options: {{
        responsive: false,
        plugins: {{
          legend: {{ display: false }}
        }}
      }}
    }});

    let isSpinning = false;
    document.getElementById('spin').onclick = function() {{
      if (isSpinning) return;
      isSpinning = true;

      const duration = 4000; // thời gian quay 4s
      const ticks = 30;      // số lần phát âm thanh "tick"
      let spins = 0;

      const tickSound = document.getElementById("tickSound");

      const targetAngle = Math.random() * 360;
      const startAngle = myChart.options.rotation || 0;
      const totalRotation = 360 * 5 + targetAngle; // quay 5 vòng + góc random
      const startTime = Date.now();

      function animate() {{
        const now = Date.now();
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easing = 1 - Math.pow(1 - progress, 3); // easeOutCubic
        const currentRotation = startAngle + totalRotation * easing;

        myChart.options.rotation = currentRotation % 360;
        myChart.update();

        // Phát âm thanh theo nhịp tick
        if (progress < 1) {{
          if (elapsed / duration * ticks > spins) {{
            tickSound.currentTime = 0;
            tickSound.play();
            spins++;
          }}
          requestAnimationFrame(animate);
        }} else {{
          // Tính kết quả
          const segmentSize = 360 / labels.length;
          const idx = Math.floor(((360 - (currentRotation % 360)) % 360) / segmentSize);
          document.getElementById('result').innerHTML = "🎉 Kết quả: " + labels[idx];
          isSpinning = false;
        }}
      }}
      animate();
    }};
    </script>
    """

    components.html(html_code, height=500)
