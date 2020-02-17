/**
 * Shared lib for API calls
 */

const REST_SERVER_URL='http://localhost:3000';

/*
 * Upload file to server
 */
export const uploadFile = (files, overwrite) => {
  var formData = new FormData();

  formData.append('overwrite', overwrite);

  files.map((file, index) => {
    formData.append('scanresults', file);
  });


  return fetch(`${REST_SERVER_URL}/upload`, {
      method: 'POST',
      body: formData,
    })
    .then(response => {
      if (response.status === 400 || response.ok) {
        return response.json();
      }
      throw Error(response.statusText);
    })
    .catch(e => {
      throw Error(e);
    });
}

/*
 * Fetch all scan results. No pagination = craycray
 */
export const fetchResults = () => {
  return fetch(`${REST_SERVER_URL}/get-results`, {
      method: 'GET'
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      }
      throw Error(response.statusText);
    })
    .catch(e => {
      throw Error(e);
    });
}
