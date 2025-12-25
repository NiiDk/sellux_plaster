# Sellux Plaster Ltd — Home of Affordable Luxury

**Sellux Plaster Ltd** is a high-end, production-grade enterprise platform designed for a premier architectural finishing and building materials company based in Accra, Ghana. 

This platform represents a "Hybrid Business Model," seamlessly merging **Digital Retail (E-commerce)** with **Bespoke Architectural Services (Custom Quotations)** and a **Luxury Portfolio Showcase**.

---

## 🏗️ Core Business Modules

### 1. Unified E-commerce Engine
*   **Dynamic Material Catalogue**: Sophisticated grid for high-quality materials (Cornices, POP, Gypsum) with real-time stock status and availability logic.
*   **Intelligent Shopping Cart**: A robust session-based cart system allowing complex multi-item material procurement.
*   **Localized Localization**: Full **Ghana Cedis (GH₵)** integration with precise Cedi-to-Pesewa conversion for financial accuracy across the Paystack API.

### 2. Paystack Ghana Financial Gateway
*   **Secure Multi-Step Checkout**: High-conversion payment flow with automated redirection to Paystack's secure environment.
*   **Server-Side Verification**: Real-time transaction verification via the `PaystackService` to eliminate payment spoofing.
*   **Webhook Resilience**: Secure, HMAC-signed webhook architecture ensures order processing even if the client's connection is interrupted.

### 3. Bespoke Design & Project Workflow
*   **Precision Requests**: Custom design portal allowing clients to upload **Site Photos** and **Inspiration Images** while defining project scope (Service Type & Square Footage).
*   **Digital Quotation Pipeline**: Integrated admin workflow to review, price, and provide architectural feedback directly to user dashboards.
*   **Zero-Friction Acceptance**: One-click "Accept Quote" functionality that automatically instantiates a payable Order within the financial system.

### 4. Architectural Showcase (Portfolio)
*   **Transformation Storytelling**: Unique "Before & After" image comparison logic to visually demonstrate craftsmanship.
*   **Inventory Cross-Linking**: Projects are technically linked to specific catalogue items, showing potential clients the exact materials used in each masterpiece.
*   **Immersive Detail**: High-resolution gallery support with mobile-optimized responsive views.

### 5. Automated Communications Engine
*   **Signal-Driven Notifications**: Asynchronous event handling via Django Signals for instant transactional Email and SMS updates.
*   **Admin Feedback Loops**: Dedicated channel for admins to provide granular order updates (e.g., "In Transit", "Site Inspection Scheduled") visible on user dashboards.

---

## 🛠️ Technical Architecture & Standards

### 🛡️ Enterprise-Grade Security
*   **Brute-Force Mitigation**: **Django Axes** integration for automated rate-limiting and account lockout protection.
*   **Production Hardening**: Strictly enforced HSTS, XSS Filtering, Content-Type Sniffing protection, and SSL redirection.
*   **CSRF Protection**: Comprehensive Cross-Site Request Forgery safeguarding across all business-critical forms.

### 🚀 High-Performance Optimization
*   **Caching Strategy**: Local-memory caching for compute-heavy architectural metadata and portfolio queries.
*   **Asset Management**: Powered by **Whitenoise** for static file compression and **Cloudinary** for CDN-delivered media optimization.
*   **Scalable Service Layer**: Decoupled business logic (`core/services.py`) allowing for future-proof integration of external APIs without refactoring.

### 🤖 AI-Ready Foundation (GPT-4 Integrated)
The architecture is powered by a dedicated `AIService` supporting:
*   **Architectural Brief Enhancement**: Automatically transforming raw user descriptions into professional design specifications.
*   **Smart Pricing Estimates**: Providing baseline architectural quotes based on localized Ghanaian market rates per Sq Ft.
*   **Automated Insights**: Ready for AI-driven blog generation and product recommendations.

---

## 🚀 Deployment & Installation

### 1. Development Environment
```bash
git clone <repository-url>
cd sellux_plaster
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Smart Environment Configuration
Create a `.env` file in the root:
```env
# System Branding
COMPANY_NAME="Sellux Plaster Ltd"

# Security
SECRET_KEY=your-secure-key
DEBUG=True

# AI Architect (OpenAI)
AI_API_KEY=sk-...

# Payment (Paystack Ghana)
PAYSTACK_PUBLIC_KEY=pk_test_...
PAYSTACK_SECRET_KEY=sk_test_...

# Storage
CLOUDINARY_URL=cloudinary://...
```

### 3. Deployment (Render Optimized)
The system features **Smart Environment Detection**. It will automatically:
*   Switch to **PostgreSQL** on Render while keeping **SQLite** for Local Dev.
*   Switch to **Cloudinary/Whitenoise** for Production Storage.
*   Enforce production security headers when `RENDER=true`.

---

## ⚖️ Legal & Compliance
Full legal suite included with the platform:
*   Terms of Service
*   Privacy & Data Protection Policy
*   Refund & Material Return Policy
*   Shipping & Site Logistics Policy

**Engineered for Sellux Plaster Ltd — Accra, Ghana.**
