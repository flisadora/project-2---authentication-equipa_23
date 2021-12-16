import "./Characters.css";
import { Container, Row, Col, Card } from "react-bootstrap";
import Image from "react-bootstrap/Image";
import { useHistory } from "react-router";

function Characters() {
  let history = useHistory();

  function handleClick(character) {
    const url = `/wiki?character=${character}`;
    history.push(url);
  }

  return (
    <Card
      style={{
        width: "70rem",
        opacity: 1,
        backgroundColor: "#000",
        marginTop: "60px",
      }}
    >
      <Card.Body>
        <Container>
          <Row>
            <Col md={4} onClick={() => handleClick("Harry James Potter")}>
              <Image
                style={{
                  boxShadow: "0px 0px 20px #E7B92A",
                  border: "1px solid #fff",
                  height: "500px",
                  marginBottom: "1rem",
                }}
                src="http://image.tmdb.org/t/p/original/f1p1So4CHlJKjLc79vP6sDJG5s6.jpg"
              />
              <p></p>
              <h1>Harry Potter</h1>
            </Col>
            <Col md={4} onClick={() => handleClick("Hermione Jean Granger")}>
              <Image
                style={{
                  boxShadow: "0px 0px 20px #E7B92A",
                  border: "1px solid #fff",
                  height: "500px",
                  marginBottom: "1rem",
                }}
                src="https://i.pinimg.com/736x/e8/ea/7e/e8ea7e29480eb862225a57f61b2f1f6a.jpg"
              />
              <p></p>
              <h1>Hermione Granger</h1>
            </Col>
            <Col md={4} onClick={() => handleClick("Ronald Bilius Weasley")}>
              <Image
                style={{
                  boxShadow: "0px 0px 20px #E7B92A",
                  border: "1px solid #fff",
                  height: "500px",
                  marginBottom: "1rem",
                }}
                src="https://i.pinimg.com/originals/f5/8c/27/f58c2783a597a11c5c1f4454e13e9d67.jpg"
              />
              <p></p>
              <h1>Ron Weasley</h1>
            </Col>
          </Row>
        </Container>
      </Card.Body>
    </Card>
  );
}

export default Characters;
