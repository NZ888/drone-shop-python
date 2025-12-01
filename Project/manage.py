import Project
from Project.loadenv import init_db
def main():
    try:
        init_db()
        Project.project.run(debug= True, port= 8000)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    main()