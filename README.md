GuideLanka - Tourist Web Application 

An AI-powered tourism platform for Yala National Park, Sri Lanka. This repository contains the Tourist Web Application modules developed as part of the GuideLanka Final Year Project.


Project Overview

"GuideLanka" is an AI-based ecosystem for rural tourism marketplace and intelligent safari optimization. The system connects tourists, rural service providers, and park authorities through AI-based service discovery and safari route optimization.



My Contribution 

Tourist User Profile & History
File: `src/pages/UserProfile.jsx`

Features:
- View and edit personal information (name, phone, profile picture)
- View all safari bookings (Upcoming / Active / Completed / Cancelled)
- Cancel bookings
- Chat with safari guides
- Track live safari location
- Profile completion status indicator
- View booking history with detailed information
- Firebase authentication integration
- Supabase database integration

Park Rules, Guidelines & Safety
File: `src/pages/ParkRules.jsx`

Features:
- Official park rules (Do's & Don'ts)
- Wildlife protection guidelines (No flash photography, keep silence, no littering)
- Visitor safety rules (Stay inside vehicle, follow the guide)
- Responsible wildlife encounter guide (Elephants, Leopards, Birds)
- Interactive Eco-Tourist Quiz
- Search and filter rules by category
- Emergency assistance & ranger support contact
- Wildlife photography rules



Tourist Authentication
Files: 
- `src/components/LoginModal.jsx`
- `src/components/GoogleBtn.jsx`

Features:
- Pop-up modal for tourist login
- One-Click Google OAuth Sign In
- Tourist privileges display
- Firebase authentication integration
- Seamless login experience

---

Information & Gallery Portal
Files:
- `src/pages/Gallery.jsx`
- `src/pages/AboutPage.jsx`
- `src/pages/FaqPage.jsx`
- `src/pages/PrivacyPage.jsx`
- `src/pages/TermsPage.jsx`

Features:

Gallery:
- Wildlife photo showcase
- Search and filter by category (Wildlife, Landscapes, Safari Life)
- Lightbox view with image details
- Share functionality

About Page:
- Information about Yala Block 5 & 6
- Park statistics
- Why book with GuideLanka
- Official DWC park entrance fees
- Call-to-action for booking

FAQ Page:
- Categorized questions (Bookings, Live Tracking, Park Guidelines)
- Interactive accordion
- Support hotline

Privacy Policy:
- Data collection and usage
- Information sharing policies
- Data security & storage

Terms of Service:
- Acceptance of terms
- Booking and payment policies
- Wildlife code of conduct


Shared Navigation & Alert Layout
Files:
- `src/components/Navbar.jsx`
- `src/components/Footer.jsx`
- `src/components/AlertModal.jsx`

Features:

Navbar:
- Responsive navigation (Mobile / Desktop)
- Session state indicator (Logged in / Logged out)
- Dynamic active link highlighting
- Mobile hamburger menu
- User profile dropdown

Footer:
- Quick links (Explore, Portals & Help)
- Contact information
- Social media links
- WhatsApp direct contact
- Privacy & Terms links

Alert Modal:
- Beautiful animated alert system
- 4 types: warning, success, error, info
- Custom icons and colors for each type

Technologies Used

React.js - Frontend framework 
React Router - Client-side routing 
Tailwind CSS - Styling 
Lucide React - Icons 
Firebase Auth - Google OAuth authentication 
Supabase - Database & backend services 
Vite - Build tool 


Project Structure

guidelanka-tourist-web-app/
├── src/
│ ├── components/
│ │ ├── AlertModal.jsx 
│ │ ├── Footer.jsx 
│ │ ├── GoogleBtn.jsx 
│ │ ├── LoginModal.jsx 
│ │ └── Navbar.jsx 
│ │
│ └── pages/
│ ├── UserProfile.jsx 
│ ├── ParkRules.jsx 
│ ├── AboutPage.jsx 
│ ├── FaqPage.jsx 
│ ├── Gallery.jsx 
│ ├── PrivacyPage.jsx 
│ └── TermsPage.jsx 
│
└── README.md



---

Getting Started

## Prerequisites
- Node.js 
- npm or yarn

## Installation

```bash
# Clone the repository
git clone https://github.com/Dilki31/https://github.com/Pathum830/GuideLanka-New.git

# Navigate to project directory
cd https://github.com/Pathum830/GuideLanka-New.git

# Install dependencies
npm install

# Run development server
npm run dev


Key Features Preview

User Profile Dashboard
- Profile completion tracking
- Booking management with expandable cards
- Status badges with color coding (Pending, Approved, Completed, Cancelled)

Park Rules & Safety
- Interactive wildlife conduct guide
- Eco-Tourist quiz with scoring
- Category-based filtering

Gallery Portal
- Beautiful wildlife photography showcase
- Category filters and search
- Full-screen lightbox view

Authentication
- Google OAuth one-click login
- Modal-based authentication
- Firebase integration


Design Features

- Responsive Design - Works on mobile, tablet, and desktop
- Glass-morphism UI - Modern frosted glass effects
- Smooth Animations - Fade-in, scale-up transitions
- Color-coded Status - Visual feedback for all states
- Modern Typography - Clean and readable fonts
- Accessibility - Semantic HTML and ARIA labels



Team

GuideLanka Final Year Project 
Institute of Technology, University of Moratuwa

Supervised by: 
Senior Lecturer Dr. Kalpana Galappaththi



License

This project is part of the GuideLanka Final Year Project at the Institute of Technology, University of Moratuwa.



Acknowledgments

- Department of Wildlife Conservation (DWC) Sri Lanka
- Yala National Park Administration
- Unsplash for wildlife photography
- All safari drivers and guides who contributed


© 2026 GuideLanka. All rights reserved.