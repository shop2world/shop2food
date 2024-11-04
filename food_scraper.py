import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def create_database():
    print("데이터베이스 생성 중...")
    conn = sqlite3.connect('food_db.sqlite3')
    c = conn.cursor()
    
    # 테이블이 이미 존재하면 삭제
    c.execute("DROP TABLE IF EXISTS foods")
    
    # 새 테이블 생성
    c.execute('''CREATE TABLE foods
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  ingredients TEXT,
                  recipe TEXT,
                  image_url TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("데이터베이스 테이블 생성 완료")

def save_to_db(foods):
    print(f"{len(foods)}개의 항목을 데이터베이스에 저장 중...")
    conn = sqlite3.connect('food_db.sqlite3')
    c = conn.cursor()
    
    for food in foods:
        try:
            c.execute('''INSERT INTO foods 
                        (name, description, ingredients, recipe, image_url)
                        VALUES (?, ?, ?, ?, ?)''', food)
            print(f"항목 저장됨: {food[0]}")
        except sqlite3.Error as e:
            print(f"데이터베이스 저장 중 오류 발생: {str(e)}")
    
    conn.commit()
    conn.close()
    print("데이터베이스 저장 완료")

def scrape_foods():
    url = "https://food.shop2world.net/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("웹 스크래핑 시작...")
    try:
        print(f"URL 접속 시도: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"응답 상태 코드: {response.status_code}")
        
        if response.status_code != 200:
            print("오류: 웹사이트에 접속할 수 없습니다.")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        print("\nHTML 구조 분석 중...")
        
        # 모든 article 태그 찾기
        all_articles = soup.find_all('article')
        print(f"발견된 article 태그 수: {len(all_articles)}")
        
        foods = []
        for idx, item in enumerate(all_articles, 1):
            try:
                print(f"\n처리 중인 항목 {idx}:")
                
                # 제목 찾기
                title = item.find(['h1', 'h2'])
                if title:
                    name = title.text.strip()
                    print(f"제목 찾음: {name}")
                else:
                    print("제목을 찾을 수 없음")
                    continue
                
                # 내용 찾기
                content = item.find('div', class_='entry-content')
                if content:
                    # 모든 텍스트 내용을 가져옴
                    text_content = content.get_text(separator='\n').strip()
                    text_blocks = [block.strip() for block in text_content.split('\n') if block.strip()]
                    
                    print("발견된 텍스트 블록:")
                    for i, block in enumerate(text_blocks):
                        print(f"블록 {i}: {block[:100]}...")  # 처음 100자만 출력
                    
                    # 내용 구분
                    description = text_blocks[1] if len(text_blocks) > 1 else ""
                    ingredients = text_blocks[2] if len(text_blocks) > 2 else ""
                    recipe = "\n".join(text_blocks[3:]) if len(text_blocks) > 3 else ""
                    
                    print(f"\n추출된 정보:")
                    print(f"설명: {description[:100]}...")
                    print(f"재료: {ingredients[:100]}...")
                    print(f"레시피: {recipe[:100]}...")
                else:
                    print("내용을 찾을 수 없음")
                    continue
                
                # 이미지 URL 찾기
                image = item.find('img')
                image_url = image['src'] if image else ""
                if image_url:
                    print(f"이미지 URL 찾음: {image_url}")
                
                foods.append((name, description, ingredients, recipe, image_url))
                print(f"항목 {idx} 추가 완료")
                
            except Exception as e:
                print(f"항목 {idx} 처리 중 오류 발생: {str(e)}")
                continue
        
        return foods
        
    except requests.exceptions.RequestException as e:
        print(f"웹 요청 중 오류 발생: {str(e)}")
        return []
    except Exception as e:
        print(f"예상치 못한 오류 발생: {str(e)}")
        return []

if __name__ == "__main__":
    try:
        print("프로그램 시작")
        create_database()
        print("데이터베이스 생성 완료")
        
        foods = scrape_foods()
        print(f"\n총 {len(foods)}개의 음식 정보 수집됨")
        
        if foods:
            save_to_db(foods)
            print("데이터베이스 저장 완료")
        
        print("프로그램 종료")
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {str(e)}")