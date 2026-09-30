# Altherix - Software Consulting Website

A professional and innovative static website for Altherix, a software consulting company based in Ooty, India, specializing in application enhancements and modernization.

## About Altherix

Altherix is a leading software consulting firm headquartered in Ooty, in the Nilgiris. Founded by Ganesh S, the company specializes in breathing new life into existing applications through strategic enhancements, seamless integrations, and innovative features.

### Our Team

- **Ganesh S** - Director & Founder: Visionary leader with 15+ years in enterprise software consulting
- **Priscilla Mathews** - Chief Financial Officer: Strategic financial leader with strong technology background
- **Muralidharan R** - Senior Software Engineer: Full-stack expert specializing in Java, React, and microservices
- **Jessy Varghese** - Software Engineer: Cloud-native development and DevOps specialist
- **Cyril Johnson** - Technical Advisor: Strategic technology advisor guiding emerging technologies and best practices
- **Rohan Raj** - Software Engineer: Backend systems specialist with expertise in APIs and data-driven applications

## Features

- **Modern Design**: Bold gradient color scheme with smooth animations
- **Fully Responsive**: Optimized for desktop, tablet, and mobile devices
- **Fast Loading**: Pure HTML, CSS, and JavaScript (no dependencies)
- **SEO Optimized**: Semantic HTML and proper meta tags
- **GitHub Pages Ready**: Deploy instantly to GitHub Pages

## Sections

1. **Hero**: Eye-catching introduction with animated floating cards
2. **Services**: Comprehensive overview of consulting services
   - Legacy System Modernization
   - Custom Feature Development
   - Integration & API Development
   - Performance Optimization
3. **Projects**: 6 featured case studies across diverse industries
   - SAP HANA Performance Optimization
   - Shopify Plus Multi-Store Integration
   - Banking Core System Enhancement
   - Hospital Management System Integration
   - Learning Management Platform Enhancement
   - Fleet Management & Route Optimization
4. **Team**: Professional profiles of all team members
5. **About**: Company highlights and value propositions
6. **Contact**: Interactive contact form with Nilgiris location
7. **Footer**: Navigation and company information

## Deployment to GitHub Pages

### Option 1: Quick Deploy

1. Create a new repository on GitHub
2. Upload all files (index.html, styles.css, script.js, README.md)
3. Go to repository **Settings** → **Pages**
4. Select **Deploy from a branch**
5. Choose **main** branch and **/ (root)** folder
6. Click **Save**
7. Your site will be live at `https://yourusername.github.io/repository-name`

### Option 2: Using Git Command Line

```bash
cd altherix-website
git init
git add .
git commit -m "Initial commit: Altherix website"
git branch -M main
git remote add origin https://github.com/yourusername/altherix.git
git push -u origin main
```

Then enable GitHub Pages in repository settings as described above.

## Customization

### Update Contact Information

Edit `index.html` in the contact section:
- Email: Line with `contact@altherix.in`
- Phone: Line with `+91 81529 23515`
- Location: Line with `Ottupattarai, Coonoor, Tamil Nadu — 643105`

### Change Colors

Edit `styles.css` root variables:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    /* Add more custom colors */
}
```

### Add/Edit Projects

Update the projects section in `index.html` with your actual case studies and client work.

### Update Team Profiles

Edit team member information in the Team section of `index.html` as the team grows or roles change.

### Connect Contact Form

The contact form currently shows a success message. To connect it to a backend:
1. Use a service like Formspree, EmailJS, or Netlify Forms
2. Update the form action in `index.html`
3. Or implement a custom backend API

## Technologies Used

- HTML5
- CSS3 (Grid, Flexbox, Animations)
- Vanilla JavaScript
- Google Fonts (Inter)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This website design is created for Altherix. Modify as needed for your use case.

## Author

Built with Claude Code
