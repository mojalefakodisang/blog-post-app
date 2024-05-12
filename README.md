# Flask Blog App

The Flask Blog App is a web application built with Flask, a lightweight Python web framework. It allows users to create and manage blog posts in a simple and intuitive way.

## Installation

To install the Flask Blog App, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/flask-blog-app.git
    ```

2. Navigate to the project directory:

    ```bash
    cd flask-blog-app
    ```

3. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Configure the application:

    - Rename the `.env.example` file to `.env`.
    - Open the `.env` file and update the necessary configuration variables, such as database connection details.

7. Initialize the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

8. Start the application:

    ```bash
    flask run
    ```

9. Open your web browser and visit `http://localhost:5000` to access the Flask Blog App.

## Usage

Once the application is installed and running, you can perform the following actions:

- Create a new blog post by clicking on the "New Post" button.
- Edit an existing blog post by clicking on the "Edit" button next to the post.
- Delete a blog post by clicking on the "Delete" button next to the post.
- View a blog post by clicking on its title.

## Contributing

If you would like to contribute to the development of the Flask Blog App, please follow the guidelines in the [CONTRIBUTING.md](./CONTRIBUTING.md) file.

## License

The Flask Blog App is open source software licensed under the [MIT License](https://opensource.org/licenses/MIT).