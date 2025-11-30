# 🔍 Smart Task Analyzer  
An intelligent system that analyzes, scores, and prioritizes tasks using multiple strategies — built using **Django REST Framework** (backend) and **HTML/CSS/JS** (frontend).

This project was developed as part of the **Singularium Internship Technical Assignment**, implementing all required features + multiple bonus enhancements.

---

## 🚀 Features

### ✅ Core Features (Assignment Requirements)
- Add tasks with:
  - Title  
  - Due date  
  - Estimated hours  
  - Importance  
  - Dependencies  
- Analyze tasks through Django REST API  
- Score tasks using **Smart Balance Algorithm**  
- Display:
  - Score  
  - Explanation  
  - Priority color (High / Medium / Low)  
- Error handling & validation  
- Responsive UI  
- JSON bulk import  

---

## 🧠 Smart Balance Algorithm

Your custom scoring system weighs:

- **Urgency** (based on business-day difference: weekend-aware)  
- **Importance** (1–10 scale)  
- **Effort penalty** (small tasks get rewarded)  
- **Dependency complexity**  
- **Penalty for overdue tasks**  



