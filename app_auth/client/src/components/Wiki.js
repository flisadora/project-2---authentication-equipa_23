import { useLocation } from "react-router";
import { useEffect, useState } from "react";
import {
  Card,
  Col,
  Container,
  Form,
  FormControl,
  Image,
  Row,
  Button,
} from "react-bootstrap";

function Wiki() {
  let location = useLocation();
  const params = new URLSearchParams(location.search);
  const character = params.get("character");
  const [state, setState] = useState();

  const [user, setUser] = useState();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));

    if (user) {
      setUser(user);
    }
  }, []);

  // Allows to do a side effect on the component
  useEffect(() => {
    async function getData() {
      const body = {
        name: character,
      };
      console.log(body);

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      };
      const resp = await fetch(
        "http://localhost:8080/server/character.php",
        requestOptions
      );

      console.log(resp);
      const json = await resp.json();
      console.log(json);

      setState(json);
      //setState(mock);
    }

    getData();
  }, [character]);

  if (!state) {
    return <h1>Loading...</h1>;
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (e.target[0].value === "") return;

    const body = {
      character: state.name,
      text: e.target[0].value,
      user: JSON.parse(localStorage.getItem("user")).username,
    };

    console.log(body);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    };
    const resp = await fetch(
      "http://localhost:8080/server/comment.php",
      requestOptions
    );

    console.log(resp);
    const json = await resp.json();
    console.log(json);

    //const status = "success";

    // {success : true, comment , date}
    // {success: false, error : msg de erro}

    if (json.success) {
      const user = JSON.parse(localStorage.getItem("user"));
      const newComment = {
        nickname: user.username,
        text: json.comment,
        date: json.date,
      };

      setState((state) => ({
        ...state,
        comments: [...state.comments, newComment],
      }));
    } else {
      console.log(json.error);
    }

    // if (status === "success") {
    //   const newComment = {
    //     nickname: user.username,
    //     text: body.text,
    //     date: new Date().toISOString(),
    //   };

    //   setState((state) => ({
    //     ...state,
    //     comments: [...state.comments, newComment],
    //   }));
    // } else if (status === "failure") {
    //   console.log("failure");
    // }
  }

  async function handleClickDelete(comment) {
    const newComments = state.comments.filter(
      (c) =>
        c.nickname !== comment.nickname ||
        c.text !== comment.text ||
        c.date !== comment.date
    );
    console.log(newComments);
    // TODO: delete comment from database
    // Enviar nickname e a date
    const body = {
      username: comment.nickname,
      date: comment.date,
    };

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    };
    const resp = await fetch(
      "http://localhost:8080/server/deleteComment.php",
      requestOptions
    );

    console.log(resp);
    const json = await resp.json();
    console.log(json);

    // Response : {deleted : true/false}

    if (json.deleted) {
      setState((state) => ({
        ...state,
        comments: newComments,
      }));
    }
  }

  return (
    <Card
      style={{
        width: "70rem",
        opacity: 1,
        backgroundColor: "#000",
        borderRadius: "20px",
        marginTop: "60px",
      }}
    >
      <Card.Body>
        <Container>
          <Row className="justify-content-md-left">
            <Col
              xs={12}
              md={4}
              lg={4}
              style={{ borderRadius: "20px", backgroundColor: "#d39e00" }}
            >
              <p></p>
              <h2
                id={"Name"}
                style={{
                  fontSize: "40px",
                  textShadow: "1px 1px 1px #fff",
                  fontFamily: "'Harry Potter', sans-serif",
                }}
              >
                {state.name}
              </h2>

              <Image
                src={state.photo}
                alt="avatar"
                id={"Img"}
                style={{
                  boxShadow: "0px 0px 20px #E7B92A",
                  border: "1px solid #fff",
                  marginBottom: "1rem",
                }}
              />

              <h4
                id={"Born"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Born: </b>
                {state.born}
              </h4>
              <h4
                id={"Blood_status"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Blood Status: </b>
                {state.blood_status}
              </h4>
              <h4
                id={"Marital_status"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                {state.marital_status}
              </h4>
              <h4
                id={"Nationality"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Nationality: </b>
                {state.nationality}
              </h4>
              <h4
                id={"Species"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Species: </b>
                {state.species}
              </h4>
              <h4
                id={"Gender"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Gender: </b>
                {state.gender}
              </h4>
              <h4
                id={"Height"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Height: </b>
                {state.height}
              </h4>
              <h4
                id={"Weight"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Weight: </b>
                {state.weight}
              </h4>
              <h4
                id={"Boggart"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Boggart: </b>
                {state.boggart}
              </h4>
              <h4
                id={"Wand"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Wand: </b>
                {state.wand}
              </h4>
              <h4
                id={"Patronus"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Patronus: </b>
                {state.patronus}
              </h4>
              <h4
                id={"Ocuppation"}
                style={{
                  fontSize: "20px",
                  textShadow: "0px 0px 2px #fff",
                }}
              >
                <b>Occupation: </b>
                {state.occupation}
              </h4>

              <p></p>
            </Col>
            <Col xs={12} md={1} lg={1}>
              {" "}
            </Col>
            <Col
              xs={12}
              md={7}
              lg={7}
              style={{
                borderRadius: "20px",
                backgroundColor: "#333",
                height: "auto",
              }}
            >
              <p></p>
              <h2
                id={"House"}
                style={{
                  textAlign: "right",
                  fontSize: "60px",
                  textShadow: "1px 1px 1px #000",
                  color: "#fff",
                  fontFamily: "'Harry Potter', sans-serif",
                }}
              >
                {state.house}
              </h2>
              <br />
              <br />
              <h4
                id={"Bio"}
                style={{
                  fontSize: "20px",
                  textShadow: "1px 1px 1px #000",
                  color: "#fff",
                  fontWeight: "normal",
                  textAlign: "justify",
                }}
              >
                {state.biography}
              </h4>
            </Col>
          </Row>
          <h1 style={{ marginTop: "10rem" }}>Comments</h1>
          <Row>
            {state.comments.map((comment, index) => {
              const condition =
                user?.role === 1 || comment.nickname === user?.username;

              return (
                <div
                  key={`${index}-${comment.text}`}
                  style={{
                    display: "flex",
                    marginBottom: "20px",
                    justifyContent: "center",
                  }}
                >
                  <div
                    style={{
                      background: "#444",
                      color: "#bbb",
                      borderRadius: "10px",
                      padding: "10px",
                    }}
                  >
                    {comment.nickname} ({comment.date}) > {comment.text}
                  </div>
                  {condition && (
                    <Button
                      style={{
                        float: "right",
                        backgroundColor: "transparent",
                        border: "0px solid #000",
                        color: "red",
                      }}
                      onClick={() => handleClickDelete(comment)}
                    >
                      <b>X</b>
                    </Button>
                  )}
                </div>
              );
            })}
          </Row>
          {user && (
            <Row
              className="justify-content-md-center"
              style={{ borderRadius: "20px", backgroundColor: "#000" }}
            >
              <Col xs={12} md={8} lg={8}>
                <Form onSubmit={handleSubmit} style={{ marginTop: "2rem" }}>
                  <Form.Group>
                    <FormControl
                      as="textarea"
                      aria-label="With textarea"
                      placeholder="Write a comment..."
                    />
                  </Form.Group>

                  <div className="form-controls">
                    <Button
                      variant="dark"
                      type="submit"
                      style={{
                        marginLeft: "30%",
                        backgroundColor: "#d39e00",
                        marginTop: "1rem",
                        width: "30%",
                      }}
                    >
                      Post
                    </Button>
                  </div>
                </Form>
              </Col>
            </Row>
          )}
        </Container>
      </Card.Body>
    </Card>
  );
}

export default Wiki;
