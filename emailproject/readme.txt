django version - 4.2.15
python version - 3.9
simple blog app using django where users can register and post blogs ,comment on blogs , like/dislike blogs.
view / edit / delete blogs there is a maintenence mode middleware which is set to false in settings.py if
changed to true the users will see site undermaintenence . There is also a automatic logout middleware
which will logout users if inactive for a certain period.Users can also
edit their details including changing their name, address,image, email and password etc.


ADMIN PANEL

***Run the seeder(seeder.py)** file to create admin the admin can view all the users their number of posts etc tha admin can delete
the registered users there is also a custom decorator for admin so that normal users cant access admin url. The admin
can lock and unlock normal users (done by ajax).

**********************ADMIN PASSWORD AND EMAIL IS IN THE SEEDER.PY FILE ************

PERMISSIONS
***run the seeder permissionseeder.py*** to add permissions to the database
Admin can on/off different permissions for users

                ******************************************************************************
**************** NOTE - YOU HAVE TO LOGIN TO THE ADMIN PANEL AND SET PERMISSION FOR USERS FIRST  **************
                *******************************************************************************

**how to run
cd emailproject
python manage.py runserver