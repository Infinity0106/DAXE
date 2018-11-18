/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require("react");

const CompLibrary = require("../../core/CompLibrary.js");

const MarkdownBlock = CompLibrary.MarkdownBlock; /* Used to read markdown */
const Container = CompLibrary.Container;
const GridBlock = CompLibrary.GridBlock;

const siteConfig = require(`${process.cwd()}/siteConfig.js`);

function imgUrl(img) {
  return `${siteConfig.baseUrl}img/${img}`;
}

function docUrl(doc, language) {
  return `${siteConfig.baseUrl}docs/${language ? `${language}/` : ""}${doc}`;
}

function pageUrl(page, language) {
  return siteConfig.baseUrl + (language ? `${language}/` : "") + page;
}

class Button extends React.Component {
  render() {
    return (
      <div className="pluginWrapper buttonWrapper">
        <a className="button" href={this.props.href} target={this.props.target}>
          {this.props.children}
        </a>
      </div>
    );
  }
}

Button.defaultProps = {
  target: "_self"
};

const SplashContainer = props => (
  <div className="homeContainer">
    <div className="homeSplashFade">
      <div className="wrapper homeWrapper">{props.children}</div>
    </div>
  </div>
);

const Logo = props => (
  <div className="projectLogo">
    <img
      src={props.img_src}
      alt="Project Logo"
      style={{ width: 300, height: 100 }}
    />
  </div>
);

const ProjectTitle = () => (
  <h2 className="projectTitle">
    {siteConfig.title}
    <small>{siteConfig.tagline}</small>
  </h2>
);

const PromoSection = props => (
  <div className="section promoSection">
    <div className="promoRow">
      <div className="pluginRowBlock">{props.children}</div>
    </div>
  </div>
);

class HomeSplash extends React.Component {
  render() {
    const language = this.props.language || "";
    return (
      <SplashContainer>
        <Logo img_src={imgUrl("logo.png")} />
        <div className="inner">
          <ProjectTitle />
          <PromoSection>
            <Button href={docUrl("doc1.html", language)}>Empieza aqui</Button>
            {/* <Button href={docUrl("doc1.html", language)}>Example Link</Button>
            <Button href={docUrl("doc2.html", language)}>Example Link 2</Button> */}
          </PromoSection>
        </div>
      </SplashContainer>
    );
  }
}

const Block = props => (
  <Container
    padding={["bottom", "top"]}
    id={props.id}
    background={props.background}
  >
    <GridBlock align="center" contents={props.children} layout={props.layout} />
  </Container>
);

const Features = () => (
  <Block layout="fourColumn">
    {[
      {
        content:
          "Todas las funciones de programacion basica, varaibles, arreglos, funciones",
        image: imgUrl("logo.png"),
        imageAlign: "top",
        title: "Programacion basica"
      },
      {
        content: "Podras crear imagenes y podras exportarlas en svg",
        image: imgUrl("logo.png"),
        imageAlign: "top",
        title: "Dibujos"
      }
    ]}
  </Block>
);

const FeatureCallout = () => (
  <div
    className="productShowcaseSection paddingBottom"
    style={{ textAlign: "center" }}
  >
    <h2>Demo</h2>

    <DemoVideo />
    {/* <MarkdownBlock>
      [![Everything Is
      AWESOME](http://i.imgur.com/Ot5DWAW.png)](https://youtu.be/StTqXEQ2l-Y?t=35s
      "Everything Is AWESOME")
    </MarkdownBlock> */}
  </div>
);

const LearnHow = () => (
  <Block background="light">
    {[
      {
        content: "Talk about learning how to use this",
        image: imgUrl("docusaurus.svg"),
        imageAlign: "right",
        title: "Learn How"
      }
    ]}
  </Block>
);

const TryOut = () => (
  <Block id="try">
    {[
      {
        content: "Talk about trying this out",
        image: imgUrl("docusaurus.svg"),
        imageAlign: "left",
        title: "Try it Out"
      }
    ]}
  </Block>
);

const Description = () => (
  <Block background="dark">
    {[
      {
        content: "This is another description of how this project is useful",
        image: imgUrl("docusaurus.svg"),
        imageAlign: "right",
        title: "Description"
      }
    ]}
  </Block>
);

const Showcase = props => {
  if ((siteConfig.users || []).length === 0) {
    return null;
  }

  const showcase = siteConfig.users
    .filter(user => user.pinned)
    .map(user => (
      <a href={user.infoLink} key={user.infoLink}>
        <img src={user.image} alt={user.caption} title={user.caption} />
      </a>
    ));

  return (
    <div className="productShowcaseSection paddingBottom">
      <h2>Quien Lo Usa?</h2>
      <p>
        Este proyecto esta enfocado hacia personas de monclova, COA, asi que
        podrian aprender las cosa basicas de programacion.
      </p>
      <div className="logos">{showcase}</div>
      {/* <div className="more-users">
        <a className="button" href={pageUrl("users.html", props.language)}>
          More {siteConfig.title} Users
        </a>
      </div> */}
    </div>
  );
};

class Index extends React.Component {
  render() {
    const language = this.props.language || "";

    return (
      <div>
        <HomeSplash language={language} />
        <div className="mainContainer">
          <Features />
          <FeatureCallout />
          {/* <LearnHow />
          <TryOut />
          <Description /> */}
          <Showcase language={language} />
        </div>
      </div>
    );
  }
}

const DemoVideo = () => {
  return (
    <div>
      <video width="50%" height="50%" playsInline loop controls>
        <source src="/video/demo.mp4" type="video/mp4" />
      </video>
    </div>
  );
};

module.exports = Index;
