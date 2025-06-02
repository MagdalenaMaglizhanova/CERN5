import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Particle Collision Simulation - CERN", layout="wide")

st.title("Particle Collision Simulation - Educational CERN Module")

st.header("What is a particle collision?")
st.markdown("""
At CERN, particle accelerators collide particles at extremely high speeds to help scientists understand the structure of matter and the universe.
Watch this short animation that shows protons colliding inside the Large Hadron Collider (LHC).
""")
st.video("https://www.youtube.com/watch?v=Yq0zeWX49SM")

st.markdown("---")

st.header("Run a collision with your own values")

col1, col2 = st.columns(2)
with col1:
    m1 = st.number_input("Mass of particle 1 (kg)", min_value=0.1, value=5.0, step=0.1)
    v1 = st.number_input("Velocity of particle 1 (m/s)", value=5.0, step=0.1)
with col2:
    m2 = st.number_input("Mass of particle 2 (kg)", min_value=0.1, value=5.0, step=0.1)
    v2 = st.number_input("Velocity of particle 2 (m/s)", value=-3.0, step=0.1)

collision_type = st.selectbox("Select collision type:", ["Elastic", "Inelastic"])

# Calculate results based on collision type
if collision_type == "Elastic":
    v1_final = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
    v2_final = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2
else:
    # Inelastic collision - particles stick together
    v_final = (m1 * v1 + m2 * v2) / (m1 + m2)
    v1_final = v_final
    v2_final = v_final

# Prepare trajectories
t = np.linspace(0, 2, 30)
if collision_type == "Elastic":
    x1 = v1 * t
    x2 = 10 + v2 * t
else:
    collision_time = 10 / (v1 - v2) if v1 != v2 else 1
    x1 = np.piecewise(t, [t < collision_time, t >= collision_time],
                      [lambda t: v1 * t, lambda t: v_final * t])
    x2 = np.piecewise(t, [t < collision_time, t >= collision_time],
                      [lambda t: 10 + v2 * t, lambda t: 10 + v_final * t])

frames = []
for i in range(len(t)):
    frames.append(go.Frame(data=[
        go.Scatter3d(x=[x1[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=10, color='blue'),
                     text=["Particle 1"], textposition="top center"),
        go.Scatter3d(x=[x2[i]], y=[0], z=[0], mode='markers+text',
                     marker=dict(size=10, color='red'),
                     text=["Particle 2"], textposition="top center")
    ]))

layout = go.Layout(
    scene=dict(
        xaxis=dict(range=[-10, 30], title='Position X'),
        yaxis=dict(range=[-5, 5], title='Y'),
        zaxis=dict(range=[-5, 5], title='Z'),
    ),
    title=f"3D Animation of {collision_type.lower()} collision",
    margin=dict(l=0, r=0, b=0, t=40),
    height=500,
    updatemenus=[dict(type="buttons", showactive=False,
                      buttons=[dict(label="▶ Play animation",
                                    method="animate",
                                    args=[None, {"frame": {"duration": 100, "redraw": True},
                                                 "fromcurrent": True}])])]
)

fig = go.Figure(
    data=[
        go.Scatter3d(x=[x1[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='blue')),
        go.Scatter3d(x=[x2[0]], y=[0], z=[0], mode='markers', marker=dict(size=10, color='red'))
    ],
    layout=layout,
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("## Collision Results")

impulse_before = m1 * v1 + m2 * v2
impulse_after = m1 * v1_final + m2 * v2_final

energy_before = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
energy_after = 0.5 * m1 * v1_final ** 2 + 0.5 * m2 * v2_final ** 2

st.write(f"**Momentum before collision:** {impulse_before:.2f} kg·m/s")
st.write(f"**Momentum after collision:** {impulse_after:.2f} kg·m/s")
st.write(f"**Kinetic energy before collision:** {energy_before:.2f} J")
st.write(f"**Kinetic energy after collision:** {energy_after:.2f} J")

energy_loss = energy_before - energy_after
if collision_type == "Inelastic":
    st.write(f"**Energy lost in collision:** {energy_loss:.2f} J (converted to heat/deformation)")

st.markdown("---")

st.header("Reflection Questions")

st.markdown("""
- Is momentum conserved?  
- Is kinetic energy conserved?  
- How do the velocities change for different collision types?  
- What does it mean if kinetic energy decreases?  
""")

st.header("Enter your hypothesis about the collision result:")

hypothesis = st.text_area("What do you expect to happen to velocities and energy?")

if st.button("Submit hypothesis"):
    if hypothesis.strip() == "":
        st.warning("Please enter your hypothesis.")
    else:
        if "hypotheses" not in st.session_state:
            st.session_state.hypotheses = []
        st.session_state.hypotheses.append(hypothesis)
        st.success("Your hypothesis has been submitted! Great job thinking actively!")

        st.markdown("### Sample hypotheses from other students:")
        for i, hyp in enumerate(st.session_state.hypotheses[-5:], 1):
            st.write(f"{i}. {hyp}")

# === Вграден THREE.js 3D particles код, показващ сблъсък ===

three_js_html = """
<div id="three-container" style="width:100%; height:600px;"></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.142.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.142.0/examples/js/controls/OrbitControls.js"></script>

<script>
  const container = document.getElementById('three-container');
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);

  const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
  camera.position.z = 60;

  const renderer = new THREE.WebGLRenderer({antialias: true});
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  const controls = new THREE.OrbitControls(camera, renderer.domElement);

  function createBeam(direction = 1) {
    const particleCount = 1000;
    const geometry = new THREE.BufferGeometry();
    const positions = [];
    const velocities = [];

    for(let i=0; i<particleCount; i++) {
      const angle = Math.random()*2*Math.PI;
      const radius = Math.random()*2;
      const z = (Math.random() - 0.5)*2;

      const x = radius * Math.cos(angle);
      const y = radius * Math.sin(angle);

      positions.push(x, y, z + direction*40);
      velocities.push(0, 0, -direction*(0.5 + Math.random()));
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('velocity', new THREE.Float32BufferAttribute(velocities, 3));

    const material = new THREE.PointsMaterial({
      color: 0x44ccff,
      size: 0.3,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending
    });

    return new THREE.Points(geometry, material);
  }

  const beam1 = createBeam(1);
  const beam2 = createBeam(-1);
  scene.add(beam1);
  scene.add(beam2);

  const starGeometry = new THREE.BufferGeometry();
  const starPositions = [];
  for(let i=0; i<200; i++) {
    starPositions.push((Math.random()-0.5)*100, (Math.random()-0.5)*100, (Math.random()-0.5)*100);
  }
  starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starPositions, 3));
  const starMaterial = new THREE.PointsMaterial({color: 0xffffff});
  const stars = new THREE.Points(starGeometry, starMaterial);
  scene.add(stars);

  function animate() {
    requestAnimationFrame(animate);

    const positions1 = beam1.geometry.attributes.position.array;
    const velocities1 = beam1.geometry.attributes.velocity.array;
    const positions2 = beam2.geometry.attributes.position.array;
    const velocities2 = beam2.geometry.attributes.velocity.array;

    for(let i=0; i<positions1.length; i+=3) {
      positions1[i+2] += velocities1[i+2];
      if(positions1[i+2] < 0) {
        positions1[i] = (Math.random()*4 - 2);
        positions1[i+1] = (Math.random()*4 - 2);
        positions1[i+2] = 40;
        velocities1[i+2] = -(0.5 + Math.random());
      }
    }
    beam1.geometry.attributes.position.needsUpdate = true;

    for(let i=0; i<positions2.length; i+=3) {
      positions2[i+2] += velocities2[i+2];
      if(positions2[i+2] > 0) {
        positions2[i] = (Math.random()*4 - 2);
        positions2[i+1] = (Math.random()*4 - 2);
        positions2[i+2] = -40;
        velocities2[i+2] = 0.5 + Math.random();
      }
    }
    beam2.geometry.attributes.position.needsUpdate = true;

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
</script>
"""

components.html(three_js_html, height=600, scrolling=False)
