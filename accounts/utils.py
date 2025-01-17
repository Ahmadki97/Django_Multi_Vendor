


def detectUser(user):
    if user.role == 1:
        redirect_Url = 'vendorDashboard'
        return redirect_Url
    elif user.role == 2:
        redirect_Url = 'custDashboard'
        return redirect_Url
    elif user.role == None and user.is_superadmin:
        redirect_Url = '/admin'
        return redirect_Url