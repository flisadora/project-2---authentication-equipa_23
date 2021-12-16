import "./Login.css";
import { Form, Button, Card } from "react-bootstrap";
import { Link, useHistory } from "react-router-dom";
import { useState } from "react";

function Login({ onSuccess }) {
  let history = useHistory();
  // hook to add a state to a component
  const [error, setError] = useState(false);

  async function handleSubmit(e) {
    // Isto irá bloquear o comportamento nativo do form (fazer um POST request com os dados de login)
    e.preventDefault();

    if (error) return;

    const body = {
      email: e.target[0].value,
      password: e.target[1].value,
    };
    console.log(body);

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    };
    const resp = await fetch(
      "http://localhost:8080/server/login.php",
      requestOptions
    );

    console.log(resp);
    const json = await resp.json();
    console.log(json);

    // The following code evaluates if the loggin is succesful or not (according to json's response)
    const status = json.loggedin;

    if (status) {
      // From JSON's response : example
      const store = {
        username: json.username,
        role: json.role,
      };
      localStorage.setItem("user", JSON.stringify(store));
      onSuccess(store.username);
      history.push("/characters");
    } else {
      setError(true);
    }
  }

  function handleChange() {
    setError(false);
  }

  return (
    <Card
      style={{
        width: "18rem",
        opacity: 1,
        borderRadius: 20,
        backgroundColor: "#d39e00",
        marginTop: "5rem",
        padding: "1rem",
        maxHeight: 500,
      }}
    >
      <Card.Body>
        <Form onSubmit={handleSubmit}>
          <h1 className="form-title">Login</h1>
          <p></p>
          <p></p>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Control
              type="email"
              placeholder="Email"
              autoComplete="off"
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Control
              type="password"
              placeholder="Password"
              autoComplete="off"
              onChange={handleChange}
            />
          </Form.Group>
          {error && (
            <p style={{ color: "red", fontWeight: "bold" }}>
              Your credentials aren't correct!
            </p>
          )}
          <div className="form-controls">
            <Button
              style={{ width: "5rem", marginLeft: "35%" }}
              variant="dark"
              type="submit"
            >
              Login
            </Button>
            <p></p>
            <Link className="continue-link" to="/characters">
              Continuar sem login
            </Link>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
}

export default Login;
