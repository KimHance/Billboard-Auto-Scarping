# 🎵 Billboard Auto Scraping API

이 프로젝트는 [KoreanThinker/billboard-json](https://github.com/KoreanThinker/billboard-json) 프로젝트에서 영감을 받아, GitHub Actions로 Billboard 차트 데이터를 자동으로 수집하고 API 형태로 제공합니다. 별도 서버 없이 GitHub를 활용합니다.

## 📡 API Endpoints

모든 데이터는 JSON 형식으로 제공되며, 아래 URL을 통해 무료로 호출 가능합니다.
**(CORS 문제없이 웹/앱 어디서든 사용 가능)**

| 차트 이름 | API URL | 업데이트 주기 (KST) |
| :--- | :--- | :--- |
| **🔥 Hot 100** | `https://KimHance.github.io/Billboard-Auto-Scarping/billboard_hot_100.json` | **매주 수요일** 오후 2시 |
| **💿 Billboard 200** | `https://KimHance.github.io/Billboard-Auto-Scarping/billboard_200.json` | **매주 수요일** 오후 2시 |
| **🌍 Global 200** | `https://KimHance.github.io/Billboard-Auto-Scarping/billboard_global_200.json` | **매주 수요일** 오후 2시 |
| **🎤 Artist 100** | `https://KimHance.github.io/Billboard-Auto-Scarping/billboard_artist_100.json` | **매주 수요일** 오후 2시 |

> ⚠️ **Note:** GitHub Pages 반영 시간에 따라 데이터 갱신에 약간의 지연이 발생할 수 있습니다.

---

## 📅 업데이트 스케줄

GitHub Actions가 아래 일정에 맞춰 스크립트를 자동 실행합니다.

*   **Weekly Scraping:** 매주 수요일 `14:00 KST` (UTC 05:00) - `Hot 100`, `Billboard 200`, `Global 200`, `Artist 100`

---

## 📦 데이터 형식 (JSON Response)

모든 응답은 `date` 필드와 `data` 배열을 포함합니다. `data` 배열의 각 객체는 차트 항목을 나타내며, 정보가 없는 필드는 `null`일 수 있습니다.

### 기본 JSON 구조

```json
{
  "date": "YYYY-MM-DD",
  "data": [
    {
      "status": "Status",
      "rank": 1,
      "title": "Song Title",
      "artist": "Artist Name",
      "image": "https://charts-static.billboard.com/img/...",
      "last_week": 2,
      "peak_position": 1,
      "peak_date": "YYYY-MM-DD",
      "debut_position": 15,
      "debut_date": "YYYY-MM-DD",
      "weeks_on_chart": 8
    },
    // ... (나머지 차트 항목들)
  ]
}
```

### 필드 설명

*   `date`: 차트 데이터 기준 날짜 (YYYY-MM-DD).
*   `rank`: 현재 순위 (Integer).
*   `title`: 곡 제목 또는 아티스트 이름 (String).
*   `artist`: 아티스트 이름 (String).
*   `image`: 앨범 커버 또는 아티스트 이미지 URL (String | null).
*   `last_week`: 지난주 순위 (Integer | null).
*   `peak_position`: 역대 최고 순위 (Integer | null).
*   `peak_date`: 최고 순위 기록 날짜 (String | null).
*   `debut_position`: 차트 데뷔 순위 (Integer | null).
*   `debut_date`: 차트 데뷔 날짜 (String | null).
*   `weeks_on_chart`: 차트 진입 주수 (Integer | null).
*   `status`: 차트 내에서의 순위 변화 (New, Rising, Falling, Steady, Re-Entry). (String).

### 예시: Hot 100 Response

```json
{
  "date": "2024-03-21",
  "data": [
    {
      "status": "Steady",
      "rank": 1,
      "title": "Beautiful Things",
      "artist": "Benson Boone",
      "image": "https://charts-static.billboard.com/img/2024/01/benson-boone-beautiful-things-950x950.jpg",
      "last_week": 2,
      "peak_position": 1,
      "peak_date": "2024-03-21",
      "debut_position": 15,
      "debut_date": "2024-01-25",
      "weeks_on_chart": 8
    },
    {
      "status": "Falling",
      "rank": 2,
      "title": "Carnival",
      "artist": "¥$: Kanye West & Ty Dolla $ign",
      "image": "https://charts-static.billboard.com/img/2024/02/kanye-west-ty-dolla-sign-carnival-950x950.jpg",
      "last_week": 1,
      "peak_position": 1,
      "peak_date": "2024-03-01",
      "debut_position": null,
      "debut_date": null,
      "weeks_on_chart": 5
    }
  ]
}
```

### 예시: Artist 100 Response

```json
{
  "date": "2024-03-21",
  "data": [
    {
      "rank": 1,
      "title": "Taylor Swift",
      "artist": "Taylor Swift",
      "image": "https://charts-static.billboard.com/img/2006/12/taylor-swift-000.jpg",
      "last_week": 1,
      "peak_position": 1,
      "peak_date": null,
      "debut_position": null,
      "debut_date": null,
      "weeks_on_chart": 500
    }
  ]
}
```

---

### 🛠 기술 스택
*   **Language:** Python 3.x
*   **Libraries:** `requests`, `beautifulsoup4`
*   **Automation:** GitHub Actions
*   **Hosting:** GitHub Pages

---

## 📄 License
이 프로젝트는 **MIT License** 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

### 🤖 Credits
This project was designed, implemented, and automatically set up by **GEMINI (Google AI)**.

---
