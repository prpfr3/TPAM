const NBBox = document.getElementById('NB');
NBBox.textContent =
  'This currently defaults to Covent Garden pending inclusion of geolocation code';

const NBBoxHeader = document.getElementById('NBHeader');
NBBoxHeader.innerHTML = '<h2>To Note</h2>';

const ListedBuildingsBox = document.getElementById('listed-buildings-box');

const spinnerBox = document.getElementById('spinner-box');
const loadBtn = document.getElementById('load-btn');
const endBox = document.getElementById('end-box');

const buildingNoteForm = document.getElementById('building-note-form');
const building_name = document.getElementById('id_name');
const building_mynotes = document.getElementById('id_mynotes');

const csrf = document.getElementsByName('csrfmiddlewaretoken');
const url = window.location.href;

const alertBox = document.getElementById('alert-box');

//Standard code for getting the csrftoken as per https://docs.djangoproject.com/en/4.0/ref/csrf/
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
const csrftoken = getCookie('csrftoken');

const likeUnlikePosts = () => {
  const likeUnlikeForms = [
    ...document.getElementsByClassName('like-unlike-forms'),
  ];
  likeUnlikeForms.forEach((form) =>
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const clickedId = e.target.getAttribute('buildings-form-id');
      const clickedBtn = document.getElementById(`like-unlike-${clickedId}`);
      $.ajax({
        type: 'POST',
        url: '/ukheritage/like-unlike/',
        data: { csrfmiddlewaretoken: csrftoken, pk: clickedId },
        success: function (response) {
          clickedBtn.textContent = response.liked
            ? `Unlike (${response.count})`
            : `Like (${response.count})`;
        },
        error: function (error) {
          console.log(error);
        },
      });
    })
  );
};

let visible = 6;

const getData = () => {
  $.ajax({
    type: 'GET',

    url: `/ukheritage/get_nearby_buildings/${visible}/`,
    success: function (response) {
      const { buildings } = response;
      spinnerBox.classList.add('not-visible');
      //console.log(buildings)
      buildings.forEach((element) => {
        ListedBuildingsBox.innerHTML += `
                    <div class="card mb-2">
                        <div class="card-body">
                            <h5 class="card-title">id: ${element.id}</h5>
                            <p class="card-text">${element.listed_building}</p>
                            <p class="card-text">${Number(
                              element.distance.toFixed(1)
                            )} metres away</p>
                        </div>
    
                        <div class="card-footer">
                            <div class="row">
                                <div class="col-2"><a href="https://historicengland.org.uk/listing/the-list/list-entry/${
                                  element.hyperlink
                                }" class="btn btn-primary">Historic England Listing</a></div>
                                <div class="col-2"><a href="${url}${
          element.id
        }" class="btn btn-primary">Listing Details</a></div>
                                <div class="col-2">
                                    <form class="like-unlike-forms" buildings-form-id="${
                                      element.id
                                    }">
                                    <button href="#" class="btn btn-primary" id="like-unlike-${
                                      element.id
                                    }">${
          element.liked
            ? `Unlike (${element.count})`
            : `Like (${element.count})`
        }</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
      });

      likeUnlikePosts();

      if (response.size === 0) {
        endBox.textContent = 'No buildings added yet....';
      } else if (response.size <= visible) {
        loadBtn.classList.add('not-visible');
        endBox.textContent = 'No more buildings to load';
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
};

loadBtn.addEventListener('click', () => {
  spinnerBox.classList.remove('not-visible');
  visible += 6;
  getData();
});

buildingNoteForm.addEventListener('submit', (e) => {
  e.preventDefault();

  $.ajax({
    type: 'POST',
    url: '',
    data: {
      csrfmiddlewaretoken: csrf[0].value,
      building_name: building_name.value,
      building_mynotes: building_mynotes.value,
    },
    success: function (response) {
      ListedBuildingsBox.insertAdjacentHTML(
        'afterbegin',
        `
                <div class="card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">id: ${response.id}</h5>
                        <p class="card-text">${response.listed_building}</p>
                    </div>

                    <div class="card-footer">
                        <div class="row">
                            <div class="col-2">
                                <a href="${
                                  response.hyperlink
                                }" class="btn btn-primary">Historic England Listing</a>
                            </div>

                            <div class="col-2">
                                <form class="like-unlike-forms" buildings-form-id="${
                                  response.id
                                }">
                                <button href="#" class="btn btn-primary" id="like-unlike-${
                                  response.id
                                }">${
          response.liked
            ? `Unlike (${response.count})`
            : `Like (${response.count})`
        }</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>            
            `
      );
      likeUnlikePosts();
      $('#addNoteModal').modal('hide');
      handleAlerts('success', 'Note Added');
      buildingNoteForm.reset();
    },
    error: function (error) {
      handleAlerts('danger', 'An error occurred');
    },
  });
});

//initial run of getData
getData();
