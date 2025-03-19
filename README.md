# 📜 Thirukkural Project  


## 🎬 **Model Demo**

https://github.com/user-attachments/assets/8f70e70c-4dc8-4408-8932-da0f231f89ef


## 🛠️ Installation  

### 🔹 **Step 1: Clone the Repository**  
```bash
git clone https://github.com/Avinash8055/Thirukkural.git
cd Thirukkural
```
### 🔹 **Step 2: Install Dependencies**  
Before running the project, install the required Python packages:  
```bash
pip install -r requirements.txt
```  

### 🔹 **Step 3: Additional Requirements**  

#### 🎵 **For Audio Processing**  
If you need **FFmpeg** for audio processing, install it on Windows:  
1. Download **FFmpeg** from: [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)  
2. Install `ffmpeg.exe` and ensure it is **added to the system PATH**.

#### 🔧 **User Configuration**  

Ensure you set up the required **ElvenLabs API keys** in an **environment file** (`.env`) or directly in your script.  

### 🔹 **Environment Variables Setup**  
Create a `.env` file in the project root and add the following:  
```ini
ELVENLABS_API_KEY=your_api_key_here
```
Also, provide the paths to the necessary files:  
- **Image file path**: `<your_image_file_path>`  
- **CSV file path**: `<your_csv_file_path>`  

## 🎨 Tkinter Information  
- **Tkinter** comes pre-installed with **Python 3.12** and **does not require installation via pip**.  
- To verify Tkinter is installed, run:  
  ```python
  import tkinter
  print(tkinter.TkVersion)
  ```
- **For Linux:** If Tkinter is missing, install it using:  
  ```bash
  sudo apt-get install python3-tk
  ```
- **For macOS:** Tkinter is included with Python by default.  

## 🚀 Running the Project  

### 🔹 **Run Thirukkural Script**  
```bash
python thirukkural.py
```
