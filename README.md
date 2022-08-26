<p align="center"> 
 <img src="https://i.ibb.co/XJcPKYv/FAAB99-2-removebg-preview.png" alt="LOGO" border="0" width=200/>&nbsp;</a></p>

<p align="center">
<a href="https://www.python.org/"><img src="https://forthebadge.com/images/badges/made-with-python.svg" border="0" title="Made with Python" />
</p>

<p align="center">
<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a>  
</p>
  
<p align="center">
<a href="https://github.com/World-Konkani-Centre/SCL-2022-AMEYA/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/World-Konkani-Centre/SCL-2022-AMEYA"></a>
<a href="https://github.com/World-Konkani-Centre/SCL-2022-AMEYA"><img alt="GitHub stars" src="https://img.shields.io/github/last-commit/World-Konkani-Centre/SCL-2022-AMEYA"></a>
<a href="https://github.com/World-Konkani-Centre/SCL-2022-AMEYA/blob/main/LICENSE.md"><img alt="GitHub License" src="https://img.shields.io/github/license/World-Konkani-Centre/SCL-2022-AMEYA?label=license"></a>
</p>

# SCL-2022-AMEYA

Nowadays, people love to travel and to run around the world. Few love adventures
places, few are nature lovers, few want relaxation and many other things. So, it is
difficult to set itinerary for their travel place although we get all details online. Here
we are with our website which helps travellers to set perfect travel plan. Website
mainly focuses on different places, near by restaurants, near by attraction etc. All the
places have clear explanation which includes description, entry fees, hours open and
so on along with maps which makes travel easy. This app also updates the user with
the rules and regulations followed at the specific place. It also provides updates on
different public transport facilities available. Also each restaurant or places have
customer review based on which you can decide on your target. All together this app
makes your searching and travelling plans both easy and cool.

1. Backend Framework: **Django**
2. Front-end Framework: **Bootstrap**

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#documentation">Documentation</a></li>
    <li><a href="#setup-guide">Setup Guide</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#project-maintainers">Project Maintainers</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

### Documentation

[Documentaion](https://yatra-mitra.notion.site/yatra-mitra/Yatra-Mitra-2f40e1de5137416b91c96bdcc709125d)

### Setup Guide

[Setup Guide](https://drive.google.com/drive/folders/1jzBBdeVNVFwFoedH8BUntDhUQIjzykV9)

### Installation

1. - Fork the [repo](https://github.com/World-Konkani-Centre/SCL-2022-AMEYA)
   - Clone the repo to your local system
   ```git
   git clone https://github.com/World-Konkani-Centre/SCL-2022-AMEYA.git
   cd SCL-2022-AMEYA
   ```
   Make sure you have python installed on your system.
2. Create a Virtual Environment for the Project

   If u don't have a virtualenv installed

   ```bash
   pip install virtualenv
   ```

   ```bash
   virtualenv env

   source env/Scripts/activate
   ```

   If you are giving a different name than `env`, mention it in `.gitignore` first

3. Install all the requirements

   ```bash
   pip install -r requirements.txt
   ```

4. Make migrations/ Create db.sqlite3

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a super user.
   This is to access Admin panel and admin specific pages.

   ```djangotemplate
   python manage.py createsuperuser
   ```

   Enter your username, email and password.

6. Run server
   ```bash
   python manage.py runserver
   ```

### Project Maintainers

| <img src = "https://avatars.githubusercontent.com/u/75678927?v=4" width="50px"> | <img src = "https://avatars.githubusercontent.com/u/57653187?v=4" width="50px"> | <img src = "https://avatars.githubusercontent.com/u/84091455?v=4" width="50px"> | <img src = "https://avatars.githubusercontent.com/u/71364468?v=4" width="50px"> | <img src = "https://avatars.githubusercontent.com/u/74701658?v=4" width="50px"> | <img src = "https://avatars.githubusercontent.com/u/100398507?v=4" width="50px"> | <img src = "https://avatars.githubusercontent.com/u/91744621?v=4" width="50px"> |
| :-----------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
|                 [Kishor Balgi](https://github.com/KishorBalgi)                  |              [Ashwin Shanbhag](https://github.com/AshwinShanbhag)               | [Prathiksha Kini](https://github.com/pkini2002)                                 | [Vinayak Shenoy](https://github.com/Vinayaka-N-Shenoy)                          | [Nima](https://github.com/Nima-ps26)                                            | [Darshan Naik](https://github.com/DarshanDattaNaik)                              | [Punya Shenoy](https://github.com/Punya-7)                                      |

### License

[GNU General Public License v3.0](https://github.com/World-Konkani-Centre/SCL-2022-AMEYA/blob/main/LICENSE.md)
