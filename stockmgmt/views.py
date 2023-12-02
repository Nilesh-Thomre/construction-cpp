from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
import boto3
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import IssueForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
 
LOGIN_REDIRECT_URL = '/login'
 
 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')  # Redirect to home page or other appropriate page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')  # Replace 'home' with the name of the view you want to redirect to
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "Invalid username or password.")
 
    return render(request, 'home.html')  # Assuming your login template is named 'login.html'

@login_required(login_url='/login/')
def home(request):
	title = 'Welcome: This is the Home Page'
	context = {
	"title": title,
	}
	return render(request, "home.html",context)
	
@login_required(login_url='/login/')
def list_item(request):
	title = 'List of Items'

	queryset = Stock.objects.all()
	context = {
		"title": title,
		"queryset": queryset,
		 
		 
	}
	

	return render(request, "list_item.html", context)

@login_required(login_url='/login/')
def add_items(request):
    form = StockCreateForm(request.POST or None)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user  # Set the user to the currently logged-in user
        instance.save()
        messages.success(request, 'Successfully added')

        return redirect('/list_item')
    
    context = {
        "form": form,
        "title": "Add Item",
    }
    
    return render(request, "add_items.html", context)

@login_required(login_url='/login/')
def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated')

			return redirect('/list_item')

	context = {
		'form':form
	}
	return render(request, 'add_items.html', context)

@login_required(login_url='/login/')
def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Successfully deleted')
		return redirect('/list_item')
	return render(request, 'delete_items.html')


@login_required(login_url='/login/')
def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = {
	
		"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)
	
# Initialize AWS SNS client
sns_client = boto3.client('sns', region_name='us-east-1')

@login_required(login_url='/login/')
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        # Assuming you have a topic ARN for the SNS topic
        topic_arn = 'arn:aws:sns:us-east-1:087976260153:22209972-cpp-SNS'

        # Sending notification via AWS SNS
        
        message = f"Issued {instance.issue_quantity} {instance.item_name}(s) successfully. "
        message += f"There are now {instance.quantity} {instance.item_name}(s) left in the store."
        sns_client.publish(TopicArn=topic_arn, Message=message)

        # Rest of your code remains the same...
        # instance.issue_by = str(request.user)
        messages.success(request, message)
        instance.save()

        return redirect('/stock_detail/' + str(instance.id))
    
    context = {
        "title": f"Issue {queryset.item_name}",
        "queryset": queryset,
        "form": form,
        "username": f"Issue By: {request.user}",
    }
    return render(request, "add_items.html", context)

@login_required(login_url='/login/')
def receive_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReceiveForm(request.POST or None, instance=queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.quantity += instance.receive_quantity
		instance.save()
		messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

		return redirect('/stock_detail/'+str(instance.id))
		# return HttpResponseRedirect(instance.get_absolute_url())
	context = {
			"title": 'Reaceive ' + str(queryset.item_name),
			"instance": queryset,
			"form": form,
			"username": 'Receive By: ' + str(request.user),
		}
	return render(request, "add_items.html", context)