from core.project_loader.loader import ProjectLoader


def main():

    loader = ProjectLoader()

    project = loader.load(
        r"D:\Projects\2d_to_3d"
    )

    print(f"Files: {project.total_files}")

    for file in project.files[:10]:
        print(file.path)


if __name__ == "__main__":
    main()