import os

def create_icons():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_dir = os.path.join(base_dir, 'web')
    
    # Beautiful Material Design Astral Hexagram / Stellar Glyph SVG Icon
    icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c1938"/>
      <stop offset="50%" stop-color="#1b3570"/>
      <stop offset="100%" stop-color="#080e21"/>
    </linearGradient>
    <linearGradient id="nebGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#d3e3fd"/>
      <stop offset="50%" stop-color="#a8c7fa"/>
      <stop offset="100%" stop-color="#7cacf8"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background squircle -->
  <rect width="512" height="512" rx="112" fill="url(#bgGrad)"/>
  <rect width="504" height="504" x="4" y="4" rx="108" fill="none" stroke="#a8c7fa" stroke-width="4" stroke-opacity="0.25"/>

  <!-- Orbital rings -->
  <circle cx="256" cy="256" r="160" fill="none" stroke="#a8c7fa" stroke-width="3" stroke-dasharray="8 12" stroke-opacity="0.35"/>
  <ellipse cx="256" cy="256" rx="190" ry="85" fill="none" stroke="#a8c7fa" stroke-width="2.5" stroke-opacity="0.4" transform="rotate(-30 256 256)"/>

  <!-- Celestial Core Stars -->
  <g filter="url(#glow)">
    <!-- Central 4-pointed Star -->
    <path d="M 256,96 Q 256,256 96,256 Q 256,256 256,416 Q 256,256 416,256 Q 256,256 256,96 Z" fill="url(#nebGrad)"/>
    <circle cx="256" cy="256" r="32" fill="#ffffff"/>
  </g>

  <!-- Satellite Nodes -->
  <circle cx="130" cy="180" r="14" fill="#a8c7fa" filter="url(#glow)"/>
  <circle cx="382" cy="332" r="14" fill="#a8c7fa" filter="url(#glow)"/>
  <circle cx="256" cy="96" r="10" fill="#ffffff"/>
  <circle cx="256" cy="416" r="10" fill="#ffffff"/>
</svg>"""

    icon_path = os.path.join(web_dir, 'icon.svg')
    favicon_path = os.path.join(web_dir, 'favicon.svg')
    
    with open(icon_path, 'w', encoding='utf-8') as f:
        f.write(icon_svg)
    with open(favicon_path, 'w', encoding='utf-8') as f:
        f.write(icon_svg)
        
    print(f"Created icons: {icon_path}")

if __name__ == '__main__':
    create_icons()
