class Contact:
    def __init__(self, name, phone, email, addr):
        # self.name과 name은 서로 다른 존재인데 할당으로 연결됨
        self.name = name
        self.phone = phone
        self.email = email
        self.addr = addr
    
    def print_info(self):
        print(f'이름: {self.name}, 전화번호: {self.phone}, 이메일: {self.email}, 주소: {self.addr}\n')
        # self.name과 name은 서로 다른 존재이므로 {self.name}과 {name}은 서로 다른 상태이다.

    @staticmethod
    def set_contact():
        name = input('이름 입력: ')
        phone = input('전화번호: ')
        email = input('이메일: ')
        addr = input('주소: ')
        contact = Contact(name, phone, email, addr)
        # Contact는 클래스명, contact는 인스턴스명이 된다.
        return contact

    @staticmethod
    def get_contact(clist):
        for i in clist:
            i.print_info() # 클래스 내부에 선언된 함수는 메소드, 클래스 바깥에 있으면 함수
    
    @staticmethod
    def del_contact(clist, name):
        for i, t in enumerate(clist): # i는 인덱스, t는 요소(인스턴스)를 출력한다.
            if t.name == name:
                del clist[i]

    @staticmethod
    def print_menu():
        print('1. 연락처 입력')
        print('2. 연락처 출력')
        print('3. 연락처 삭제')
        print('4. 종료')
        menu = input('메뉴선택: ')
        return menu

    @staticmethod
    def run():
        clist = []
        while 1:
            menu = Contact.print_menu()
            if menu == '1':
                t = Contact.set_contact()
                clist.append(t)

            if menu == '2':
                Contact.get_contact(clist) # static method는 클래스가 직접 접근
            
            if menu == '3':
                name = input('삭제할 연락처의 이름을 입력해주세요: ')
                Contact.del_contact(clist, name)

            if menu == '4':
                break

if __name__ == '__main__':
    Contact.run()
    