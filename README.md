## 🚀 Haazrri - Smart Attendance System  
📌 A smart way to **prevent proxies** in attendance marking!

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)  ![Flask](https://img.shields.io/badge/Flask-3.1-lightgreeny?style=for-the-badge) 


Keeping track of student attendance while preventing proxies is a labor-intensive and manual task for teachers. **Haazrri** is designed to solve this problem by providing a **complete attendance and anti-proxy solution**.


## ⚡Features

- **Proxy Prevention** using FPS-based pattern matching  
- **Email and Password Validation** for secure access  
- **Role-Based Access Control** with separate functionalities for students and teachers
- 
 ## ⚡Future scope
- **Dashboard** for efficient attendance tracking
- **IP address based authentication** for preventing proxy login
- **Facial recognition** 

## 💡Anti-Proxy System

**Haazrri** is primarily designed to prevent proxy attendance using a **video pattern recognition system**.

### How It Works:

1. **Pattern Generation**:  
   - When a teacher clicks **“Create Attendance”**, Haazrri generates a randomized black-and-white frame pattern at a random FPS (frames per second) between **20 and 30**.
   
2. **Attendance Marking**:  
   - When a student clicks **“Mark Attendance”**, their phone camera opens, and a recording of the displayed pattern is captured.

3. **Pattern Recognition & Verification**:  
   - The backend, powered by **OpenCV**, processes the recorded sequence.  
   - If the captured pattern matches the generated one, attendance is marked successfully.  
   - If mismatched, the student must retry.

### Why It Prevents Proxy Attendance:

 
- **Synchronization Requirement**: The student's camera must match the generated FPS exactly.  
- **Proxy Attempts via Video Calls Fail**:  
  - Video calls introduce **FPS fluctuations** due to network instability.  
  - Manually setting and maintaining an exact FPS in a video call is **not practically possible**.  
  - Any **frame duplication or loss** corrupts the pattern, preventing proxy attendance.

By leveraging these techniques, **Haazrri ensures that only students who are physically present can successfully mark attendance.**


## Necessary requirements (only for localhost)
1. python (with pip or conda)
2. flask
3. javascript 
4. requirements.txt

##  🔧 Usage and Installation

The website is hosted on **https://haazrri.pythonanywhere.com/**

***For localhost :***

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### **2. Create a Virtual Environment (Optional but Recommended)**  
for pip users
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```
for conda users
```bash
conda create --name haazrri-env python=3.12
conda activate haazrri-env
```

### **3. Install Dependencies**  
for pip users
```bash
pip install -r requirements.txt
```

for conda users
```bash
conda env create -f environment.yml
```

### **4. Run the Application**  
```bash
python app.py
``` 
### Video demo

**https://youtu.be/bQh4RiyBRRs?si=CO54W581eoYYxCn9**
---


