console.log('aashu')

let projectsUrl = 'http://127.0.0.1:8000/api/projects/'

let getProjects = () => {

    fetch(projectsUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildProjects(data)
        })

}
getProjects()




let buildProjects = (projects) => {
let projectsWrapper = document.getElementById('aashu')
projectsWrapper.innerHTML = ''
for (let i = 0; projects.length > i; i++) {
    let project = projects[i]

    let projectCard = `
            <div class="card" style="width:18rem">
                <img  src="http://127.0.0.1:8000${project.featured_image}"  class="card-img-top"/>
                
                <div class="card-body">
                    <div class="card-title">
                        <h3>${project.title}</h3>
                        <strong class="vote--option" data-vote="up" data-project="${project.id}" >&#43;</strong>
                        <strong class="vote--option" data-vote="down" data-project="${project.id}"  >&#8722;</strong>
                    </div>
                    <i>${project.vote_ratio}% Positive feedback </i>
                    <p>${project.description.substring(0, 150)}</p>
                </div>
            
            </div>

            <div class="col-md-4">
            <div class="card m-3" style="width: 18rem;">
              <a href="{% url 'project' project.id%}" class="project" style="text-decoration:none">
                <img class="card-img-top" src="${ project.featured_image.url }" alt="project thumbnail" width="200" height="200" />
                <div class="card__body">
                  <h3 class="project__title">${project.title}</h3>
                  <p><a class="project__author" href="{% url 'user-profile' project.owner.id %}">By
                    ${project.owner.name}</a></p>
                  <p class="project--rating">
                    <span style="font-weight: bold;">${project.vote_ratio}%</span> Postive
                    Feedback ({{project.vote_total}} Votes)
                  </p>
                  <div class="project__tags my-2">
                    {% for tag in project.tags.all %}
                   <span class="badge bg-success">
                      <strong>{{tag}}</strong>
                    </span>
                    {% endfor %}
                    
                  </div>
                </div>
              </a>
            </div>
          </div>
    `
    projectsWrapper.innerHTML += projectCard
}



//Add an listener
}

