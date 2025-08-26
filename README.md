# KCI_RV_Framework
This repository provides a pilot implementation of a multi-agent evaluation framework for assessing the trustworthiness of Large Language Models (LLMs) in medical domains.   
# Medical LLM Trustworthiness Evaluation – Pilot Code

This repository provides a **pilot implementation** of a multi-agent evaluation framework for assessing the trustworthiness of Large Language Models (LLMs) in medical domains.  

### 🔎 Purpose
- Demonstrate how diagnostic responses from LLMs can be evaluated using a **multi-dimensional rubric** (Accuracy, Explainability, Consistency, Safety).  
- Compare **external evaluation** and **self-evaluation** (LLM self-critique), showing their differences and complementarity.  
- Provide pilot results as a proof-of-concept for the proposed framework in our research paper.

### 📂 Dataset
- The pilot uses **open clinical QA datasets** (e.g., MedQA) as substitutes for real-world diagnostic cases.  
- Each case is structured into JSON format including:  
  - `summary`  
  - `evidence_list`  
  - `criteria`  
  - `final_judgment`  

### ⚙️ Usage
1. Install dependencies  
   ```bash
   pip install -r requirements.txt

---

### 한국어 (README)
# 의료 LLM 신뢰성 평가 – 파일럿 코드

이 저장소는 의료 분야에서 대규모 언어모델(LLM)의 **신뢰성 평가를 위한 멀티에이전트 프레임워크**를 파일럿으로 구현한 코드입니다.  

### 🔎 목적
- 임상 응답(진단 텍스트)을 **다차원 루브릭**(정확성, 설명가능성, 일관성, 안전성)으로 평가하는 방법을 시연합니다.  
- **외부 평가자 평가**와 **LLM 자기 평가(Self-Critique)** 결과를 비교하여 차이점을 확인합니다.  
- 연구 논문에서 제안하는 평가 체계의 개념 증명(Proof-of-Concept)을 제공합니다.  

### 📂 데이터셋
- 실제 임상 데이터를 대체하기 위해 **공개 임상 QA 데이터셋**(MedQA)을 사용했습니다.  
- 각 케이스는 JSON 형식으로 구성됩니다:  
  - `summary`  
  - `evidence_list`  
  - `criteria`  
  - `final_judgment`  

### ⚙️ 실행 방법
1. 필수 라이브러리 설치  
   ```bash
   pip install -r requirements.txt


