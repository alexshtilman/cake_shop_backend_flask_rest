$("input:text").click(function () {
  $(this).parent().find("input:file").click();
});
$("#selectFile").click(function () {
  $(this).parent().find("input:file").click();
});
$("input:file", ".ui.action.input").on("change", function (e) {
  const name = e.target.files[0].name;
  $("input:text", $(e.target).parent()).val(name);
});
$(".button").popup();
$("#status_red").popup();
$("#status_green").popup();
function logout() {
  localStorage.setItem("t-systems", null);
  $("#progress")
    .removeClass("ui active centered inline loader red message")
    .text("");
  user_id = "";
  session_id = "";
  step = "";
  username = "";
  render(false);
}

function render(token) {
  if (token) {
    $("#sessions").removeClass("hidden");
    $("#upload").removeClass("hidden");
    $("#info").removeClass("hidden");
    $("#api").removeClass("hidden");
    $("#loggedMenu").removeClass("hidden");
    $("#login").addClass("hidden");
  } else {
    clearTable();
    $("#sessions").addClass("hidden");
    $("#upload").addClass("hidden");
    $("#info").addClass("hidden");
    $("#api").addClass("hidden");
    $("#loggedMenu").addClass("hidden");
    $("#login").removeClass("hidden");
  }
}

function clearTable() {
  const tbodymain = document.getElementById("tbodymain");
  tbodymain.innerHTML = "";
  const tr = document.createElement("tr");
  const td = document.createElement("td");
  td.setAttribute("colspan", "7");
  const div = document.createElement("div");
  div.setAttribute("class", "ui active centered inline loader");
  tr.append(td);
  td.append(div);

  tbodymain.append(tr);
}

function authorize() {
  async function start() {
    const authToken = await localStorage.getItem("t-systems");
    if (authToken !== "null" && authToken) {
      render(true);
      const jwtBody = JSON.parse(atob(authToken.split(".")[1]));
      user_id = jwtBody.identity["user_id"];
      if (!user_id) render(false);
      else {
        let response = await fetch("/sessions/" + user_id, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        let data = await response.json();
        if (response.status === 401) {
          logout();
        } else {
          const tbodymain = document.getElementById("tbodymain");
          tbodymain.innerHTML = "";
          clearTable();
          document.getElementById("upload_button").removeAttribute("disabled");
          tbodymain.innerHTML = "";
          if (data) {
            if (data.sessions.length) {
              step = data.sessions[0]["steps"];
              session_id = data.sessions[0]["session_id"];
              data.sessions.map((session) => {
                appendStr(session);
              });
            } else {
              step = data.sessions["steps"];
              session_id = data.sessions["session_id"];
              appendStr(data.sessions);
            }
          }
        }
      }
    } else render(false);
  }
  render(false);
  start();
}
authorize();

let username = "";
let password = "";
let user_id = "";
let step = "";
let session_id = "";

function createTdTh(tr, text, type = "td") {
  let td = document.createElement(type === "td" ? "td" : "th");
  td.innerText = text;
  tr.append(td);
}

function createTh(tr, text) {
  let td = document.createElement("th");
  td.innerText = text;
  tr.append(td);
}

function appendStr(record) {
  let tbodymain = document.getElementById("tbodymain");
  let tr = document.createElement("tr");
  let td = document.createElement("td");
  let i = document.createElement("i");
  i.setAttribute("class", "minus square outline icon");
  td.append(i);
  tr.append(td);

  createTdTh(tr, record["session_id"]);
  createTdTh(tr, record["name"]);
  createTdTh(tr, record["timestamp_start"]);
  createTdTh(tr, record["timestamp_end"]);
  createTdTh(tr, record["steps"]);
  createTdTh(tr, record["user_id"]);
  tbodymain.append(tr);

  let trcolspan = document.createElement("tr");
  let tdcolspan = document.createElement("td");
  tdcolspan.setAttribute("colspan", "6");
  createTdTh(trcolspan, "");
  let table = document.createElement("table");
  table.setAttribute("class", "ui celled table");
  let thead = document.createElement("thead");
  let tbody = document.createElement("tbody");
  let trHeader = document.createElement("tr");

  tbodymain.append(trcolspan);
  trcolspan.append(tdcolspan);

  tdcolspan.append(table);

  createTdTh(trHeader, "step", "th");
  createTdTh(trHeader, "data_id", "th");
  createTdTh(trHeader, "timestamp_in", "th");
  createTdTh(trHeader, "json_massive_in/out", "th");
  createTdTh(trHeader, "timestamp_out", "th");
  createTdTh(trHeader, "description", "th");
  table.append(thead);
  thead.append(trHeader);
  table.append(tbody);
  record.sequences.map((sequence) => {
    let trS = document.createElement("tr");
    createTdTh(trS, sequence["step"]);
    createTdTh(trS, sequence["data_id"]);
    createTdTh(trS, sequence["datasets"][0]["timestamp_in"]);
    let dbButton = document.createElement("td");
    let button = document.createElement("button");
    button.setAttribute("class", "ui mini icon button basic blue");
    button.innerText = "подробнее ";
    let icon = document.createElement("i");
    icon.setAttribute("class", "search plus icon");
    button.append(icon);
    button.addEventListener("click", () => {
      showJson(sequence["data_id"], record["session_id"]);
    });
    dbButton.append(button);
    trS.append(dbButton);
    createTdTh(trS, sequence["datasets"][0]["timestamp_out"]);
    createTdTh(trS, sequence["datasets"][0]["description"]);
    tbody.append(trS);
  });
}

$("#username").change((e) => {
  username = e.target.value;
});
$("#password").change((e) => {
  password = e.target.value;
});
$("#loginButton").click(() => {
  username = document.getElementById("username").value;
  password = document.getElementById("password").value;
  let options = { username: username, password: password };
  $("#progress")
    .addClass("ui active centered inline loader")
    .removeClass("red message")
    .text("");
  render(false);
  async function login() {
    let response = await fetch("/auth", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(options),
    });
    if (response.status != 401) {
      let data = await response.json();

      let authToken = data.access_token;
      const jwtBody = JSON.parse(atob(authToken.split(".")[1]));
      user_id = jwtBody.identity["user_id"];
      await localStorage.setItem("t-systems", authToken);

      render(true);

      let sessionList = await fetch("/sessions/" + user_id, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      let sessionListData = await sessionList.json();
      const tbodymain = document.getElementById("tbodymain");
      tbodymain.innerHTML = "";
      clearTable();
      document.getElementById("upload_button").removeAttribute("disabled");
      tbodymain.innerHTML = "";
      if (sessionListData) {
        if (sessionListData.sessions.length) {
          step = sessionListData.sessions[0]["steps"];
          session_id = sessionListData.sessions[0]["session_id"];
          sessionListData.sessions.map((session) => {
            appendStr(session);
          });
        } else {
          step = sessionListData.sessions["steps"];
          session_id = sessionListData.sessions["session_id"];
          appendStr(sessionListData.sessions);
        }
      }
      $("#logout").on("click", () => {
        logout();
      });
    } else {
      $("#progress")
        .removeClass("ui active centered inline loader")
        .addClass("ui red message")
        .text("Не правильный логин или пароль");
    }
  }
  login();
});

function showLoading() {
  $("#details").modal("show");
  let Jbody = document.getElementById("JSON_massive");
  Jbody.innerHTML = "";
  let div = document.createElement("div");
  div.setAttribute("class", "ui active inverted dimmer");
  let divLoader = document.createElement("div");
  let blankp = document.createElement("p");
  divLoader.setAttribute("class", "ui text loader");
  divLoader.innerHTML = "Загрузка...";
  div.append(divLoader);
  div.append(blankp);
  div.append(blankp);
  Jbody.append(div);
}

function showJson(data_id, session_id) {
  showLoading();

  async function fetchDataSet(data_id, session_id) {
    const authToken = await localStorage.getItem("t-systems");

    let response = await fetch(
      "/dataset?data_id=" + data_id + "&session_id=" + session_id,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      }
    );
    let Jbody = document.getElementById("JSON_massive");
    let result = await response.json();
    Jbody.innerHTML = "";
    let segment = document.createElement("div");
    segment.setAttribute("class", "ui segment");
    let label = document.createElement("a");
    label.setAttribute("class", "ui ribbon label blue");
    label.innerHTML = "File in";
    let container = document.createElement("div");
    container.innerText = JSON.stringify(result.dataset.json_massive_in);

    Jbody.append(segment);
    segment.append(label);
    segment.append(container);

    let segment2 = document.createElement("div");
    segment2.setAttribute("class", "ui segment");
    let label2 = document.createElement("a");
    label2.setAttribute("class", "ui ribbon label green");
    label2.innerHTML = "File out";
    let container2 = document.createElement("div");
    container2.innerText = JSON.stringify(result.dataset.json_massive_out);
    Jbody.append(segment2);
    segment2.append(label2);
    segment2.append(container2);
  }
  fetchDataSet(data_id, session_id);
}
let formElem = document.getElementById("submitForm");

formElem.onsubmit = async (e) => {
  const authToken = await localStorage.getItem("t-systems");
  if (authToken !== "null") {
    e.preventDefault();
    showLoading();
    let formData = new FormData(formElem);
    formData.append("session_id", session_id);
    formData.append("format", "upload");

    let response = await fetch("/create_dataset", {
      method: "POST",
      body: formData,
      enctype: "multipart/form-data",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    let result = await response.json();
    let Jbody = document.getElementById("JSON_massive");
    Jbody.innerHTML = result.msg;
    formElem.reset();

    let sessionList = await fetch("/sessions/" + user_id, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
    let sessionListData = await sessionList.json();
    const tbodymain = document.getElementById("tbodymain");
    tbodymain.innerHTML = "";
    clearTable();
    document.getElementById("upload_button").removeAttribute("disabled");
    tbodymain.innerHTML = "";
    if (sessionListData) {
      if (sessionListData.sessions.length) {
        step = sessionListData.sessions[0]["steps"];
        session_id = sessionListData.sessions[0]["session_id"];
        sessionListData.sessions.map((session) => {
          appendStr(session);
        });
      } else {
        step = sessionListData.sessions["steps"];
        session_id = sessionListData.sessions["session_id"];
        appendStr(sessionListData.sessions);
      }
    }
  }
};
