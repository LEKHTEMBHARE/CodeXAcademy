import os
import glob
import re
import json

base_url = "https://nextgencoding.vercel.app"

pages_config = {
    "index.html": {
        "title": "Code For Simples | Top Web Development, Python & AI Training",
        "desc": "Master Web Development, Python, Full Stack Development, and AI at Code For Simples. Join our industry-level mentorship and internship training to become job-ready."
    },
    "about.html": {
        "title": "About Us | Code For Simples - Expert IT Training",
        "desc": "Learn about Code For Simples, our mission, expert instructors, and why we are the best choice for aspiring software developers and AI engineers."
    },
    "contact.html": {
        "title": "Contact Us | Code For Simples",
        "desc": "Get in touch with Code For Simples for course inquiries, mentorship details, and internship opportunities. We are here to help."
    },
    "register.html": {
        "title": "Register Now | Enroll in Code For Simples Courses",
        "desc": "Secure your spot at Code For Simples. Register today for classes in Web Development, Python, Full Stack, and Artificial Intelligence."
    },
    "services.html": {
        "title": "Our Services | Code For Simples Mentorship & Training",
        "desc": "Explore our premium services including AI career assistance, real-world industry projects, and hands-on skill training."
    },
    "Courses\\courses.html": {
        "title": "Our Courses | Web Dev, Full Stack, Python & AI",
        "desc": "Browse professional courses offered by Code For Simples. Advance your career with expert-led training in coding and machine learning."
    },
    "Events\\events.html": {
        "title": "Upcoming Events & Workshops | Code For Simples",
        "desc": "Join Code For Simples for exclusive seminars, coding workshops, and networking events for developers and AI enthusiasts."
    },
    "Team\\team.html": {
        "title": "Meet the Team | Code For Simples Expert Mentors",
        "desc": "Meet our dedicated team of professional developers, AI researchers, and mentors who guide our students to successful careers."
    }
}

html_files = glob.glob("**/*.html", recursive=True)

manifest = {
  "name": "Code For Simples",
  "short_name": "Code For Simples",
  "description": "Premium coding & AI academy for future-ready talent.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/Code for Simple logo.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/Code for Simple logo.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}

with open("manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

for file in html_files:
    # Get config
    conf = pages_config.get(file)
    if not conf:
        # fallback for any missed file
        conf = {
            "title": "Code For Simples",
            "desc": "Code For Simples - Future ready coding and AI training."
        }
    
    file_path_url = file.replace("\\", "/")
    if file_path_url == "index.html":
        canonical_url = f"{base_url}/"
    else:
        canonical_url = f"{base_url}/{file_path_url}"
        
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create new SEO head tags
    schema_markup = {
      "@context": "https://schema.org",
      "@type": "EducationalOrganization",
      "name": "Code For Simples",
      "url": base_url,
      "logo": f"{base_url}/Code for Simple logo.png",
      "sameAs": [
        "https://www.linkedin.com/company/code-for-simples-academy"
      ]
    }
    
    seo_tags = f"""
  <!-- SEO Tags by Code For Simples -->
  <title>{conf['title']}</title>
  <meta name="title" content="{conf['title']}" />
  <meta name="description" content="{conf['desc']}" />
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
  <link rel="canonical" href="{canonical_url}" />
  
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:title" content="{conf['title']}" />
  <meta property="og:description" content="{conf['desc']}" />
  <meta property="og:image" content="{base_url}/Code for Simple logo.png" />
  <meta property="og:site_name" content="Code For Simples" />

  <meta property="twitter:card" content="summary_large_image" />
  <meta property="twitter:url" content="{canonical_url}" />
  <meta property="twitter:title" content="{conf['title']}" />
  <meta property="twitter:description" content="{conf['desc']}" />
  <meta property="twitter:image" content="{base_url}/Code for Simple logo.png" />

  <meta name="theme-color" content="#05060a" />
  <link rel="apple-touch-icon" href="/Code for Simple logo.png" />
  <link rel="manifest" href="/manifest.json" />
  
  <script type="application/ld+json">
{json.dumps(schema_markup, indent=2)}
  </script>
"""

    # Cleanup existing meta title/desc/og to avoid duplicates
    content = re.sub(r'<title>.*?</title>', '', content, flags=re.IGNORECASE | re.DOTALL)
    content = re.sub(r'<meta\s+name="title".*?>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+name="description".*?>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+property="og:.*?/>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<meta\s+property="twitter:.*?/>', '', content, flags=re.IGNORECASE)
    
    # Insert new SEO tags before </head>
    content = content.replace("</head>", seo_tags + "</head>")
    
    # Accessibility: Ensure all images have alt text (basic injection if missing)
    # This regex looks for <img> without alt=
    def add_alt(match):
        img_tag = match.group(0)
        if 'alt=' not in img_tag.lower():
            # append alt="" before the closing >
            return img_tag[:-1] + ' alt="Code For Simples Content">'
        return img_tag
        
    content = re.sub(r'<img[^>]+>', add_alt, content, flags=re.IGNORECASE)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("SEO update applied successfully.")
