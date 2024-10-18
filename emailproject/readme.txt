simple blog app using django where users can register and post blogs , like/dislike blogs(done by ajax) . There is an admin panel
run the seeder file to create admin the admin can view all the users their number of posts etc tha admin can delete
the registered users there is also a custom decorator for admin so that normal users cant access admin url. There
is also a maintenence mode middleware which is set to false in settings.py if chnaged to true the users will see site under
maintenence . There is also a automatic logout middleware which will logout users if inactive for a certain period.Users
can also edit thier details including changing their email and password. The admin can lock and unlock normal users (done by ajax).

