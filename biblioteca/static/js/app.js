function show_student_form(group) {
    const studentForm = document.getElementById('student');
    
    if (group === 'Estudante') {
        studentForm.style.display = 'flex';   
    }else {
        studentForm.style.display = 'none'
    }
}