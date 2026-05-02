from datetime import datetime
from django.shortcuts import render, redirect
from django.tasks import task
from django.views import View
from .models import task_repo, UserTask


class TaskListView(View):
    def get(self, request):
        return render(request, 'task_list.html', {'tasks': task_repo.tasks.values()})
    
class TaskCreateView(View):
    def get(self, request):
        return render(request, 'task_form.html')
    
    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if title and text and start_date_str and end_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                new_task = UserTask(
                    name=title, 
                    text=text, 
                    start_date=start_date, 
                    end_date=end_date
                )
                task_repo.add(new_task)
                return redirect('task_list')
            except ValueError:
                return render(request, 'task_form.html', {'error': 'Неверный формат даты'})
            
        return render(request, 'task_form.html', {'error': 'Заполните все поля'})
    
class TaskDeleteView(View):
    def post(self, request, task_id:int):
        task_repo.delete_by_id(task_id)
        return redirect('task_list')