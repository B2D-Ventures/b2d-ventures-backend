<!-- Improved compatibility of back to top link -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/B2D-Ventures/b2d-ventures-docs/blob/main/assets/images/logo.png">
    <img src="https://raw.githubusercontent.com/B2D-Ventures/b2d-ventures-docs/main/assets/images/logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">B2D Ventures Backend</h3>
  <p align="center">
    A backend implementation for B2D Ventures.
    <br />
    <a href="https://github.com/B2D-Ventures/b2d-ventures-backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/B2D-Ventures/b2d-ventures-backend/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/B2D-Ventures/b2d-ventures-backend/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#technology-stack">Technology Stack</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#running-the-application">Running the Application</a></li>
    <li><a href="#testing">Testing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This repository contains the backend implementation for B2D Ventures, designed to support various functionalities and services for the platform.

### Built With
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Google OAuth](https://developers.google.com/identity/protocols/oauth2)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTALLATION -->
## Installation

Follow these steps to set up the backend environment for B2D Ventures:

### Prerequisites
- Python 3.x
- pip
- Virtualenv (optional)
- Docker (optional)

### Steps
1. **Clone the Repository**
    ```
    git clone https://github.com/B2D-Ventures/b2d-ventures-backend.git
    cd b2d-ventures-backend
    ```
2. **Set Up a Virtual Environment (Optional)**
- Create a virtual environment:
    ```
    python3 -m venv venv
    ```
- Activate the virtual environment:
- On Windows:
    ```
    venv\Scripts\activate
    ```
- On MacOS/Linux:
    ```
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Environment Variables**
   - Set up your environment variables in a `.env` file (this should include sensitive information).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- RUNNING THE APPLICATION -->
## Running the Application

1. **Database Migrations**
- Before using the application, apply database migrations:
    ```
    python manage.py migrate
    ```

2. **Load Initial Data**
- Load initial data from a JSON file (ask the owner for the file):
    ```
    python manage.py loaddata db_dump.json
    ```

3. **Create Mock Data (Optional)**
- If you want to add mockup data:
    ```
    python manage.py create_mock_deals
    ```

4. **Run the Server**
- Start the development server:
    ```
    python manage.py runserver
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TESTING -->
## Testing

To run the tests, execute the following command:
```
python manage.py test b2d_ventures/app/tests/*
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/othneildrew/Best-README-Template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=B2D-Ventures/b2d-ventures-backend" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

 - [Krittin Setdhavanich](https://www.linkedin.com/in/jwizzed/)
 - [Yanatchara Jeraja](https://www.linkedin.com/in/yanatchara47/)
 - [Tantikon Phasanphaengsi](https://www.linkedin.com/in/tantikon-phasanphaengsi-b10ab825b/)

Project Link: [https://github.com/your_username/b2d-ventures-backend](https://github.com/your_username/b2d-ventures-backend)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

- [Choose an Open Source License](https://choosealicense.com)
- [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
- [Django Documentation](https://docs.djangoproject.com/en/stable/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/B2D-Ventures/b2d-ventures-backend.svg?style=for-the-badge
[contributors-url]: https://github.com/B2D-Ventures/b2d-ventures-backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/B2D-Ventures/b2d-ventures-backend.svg?style=for-the-badge
[forks-url]: https://github.com/B2D-Ventures/b2d-ventures-backend/network/members
[stars-shield]: https://img.shields.io/github/stars/B2D-Ventures/b2d-ventures-backend.svg?style=for-the-badge
[stars-url]: https://github.com/B2D-Ventures/b2d-ventures-backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/B2D-Ventures/b2d-ventures-backend.svg?style=for-the-badge
[issues-url]: https://github.com/B2D-Ventures/b2d-ventures-backend/issues
[license-shield]: https://img.shields.io/github/license/B2D-Ventures/b2d-ventures-backend.svg?style=for-the-badge
[license-url]: https://github.com/B2D-Ventures/b2d-ventures-backend/blob/master/LICENSE.txt
