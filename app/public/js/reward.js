let currentLanguage = getBrowserLanguage() || 'en';

function getBrowserLanguage() {
  // Versuche, die bevorzugte Sprache des Browsers zu erhalten
  let browserLanguage = navigator.language || navigator.userLanguage;

  if (
    browserLanguage &&
    (browserLanguage === 'de' || browserLanguage.startsWith('de-'))
  ) {
    return 'de';
  } else {
    return 'en';
  }
}
// Function to change the language
/*
function changeLanguage(lang) {
    currentLanguage = lang;
    loadContentReward();
}
*/

// Function to load content based on the selected language
function loadContentReward() {
  console.log('Loading content (reward) for language:', currentLanguage);
  fetch('language/reward_language-data.json')
    .then((response) => response.json())
    .then((data) => {
      const navbarData = data[currentLanguage].navbar;
      const GreyboxData = data[currentLanguage].Greybox;
      updateContent(navbarData);
      updateGreybox(GreyboxData);
    })
    .catch((error) =>
      console.error('Error loading language data file:', error)
    );
}

// Function to update the Introduction content on the page
function updateContent(data) {
  document.getElementById('nav-home').innerText = data.home;
  document.getElementById('nav-about').innerText = data.about;
  document.getElementById('nav-contact').innerText = data.contact;
}

// Function to update the greybox content on the page
function updateGreybox(data) {
  document.getElementById('geschenke').innerText = data.geschenke;
  //document.getElementById('about_text').innerHTML = data.about_text;
  // document.getElementById('fhome').innerText = data.fhome;
  // document.getElementById('fabout').innerText = data.fabout;
  // document.getElementById('fcontact').innerText = data.fcontact;
  // document.getElementById('fmore').innerText = data.fmore;
}

var svg = d3.select('svg'),
  margin = 20,
  diameter = +svg.attr('width'),
  g = svg
    .append('g')
    .attr('transform', 'translate(' + diameter / 2 + ',' + diameter / 2 + ')');

var color = d3
  .scaleLinear()
  .domain([-1, 5])
  .range(['#D33A80', '#FFF9F8'])
  .interpolate(d3.interpolateHcl);

var pack = d3
  .pack()
  .size([diameter - margin, diameter - margin])
  .padding(2);

d3.json('data/teethbrush.json', function (error, root) {
  if (error) throw error;

  root = d3
    .hierarchy(root)
    .sum(function (d) {
      return d.size;
    })
    .sort(function (a, b) {
      return b.value - a.value;
    });

  var focus = root,
    nodes = pack(root).descendants(),
    view;

  var circle = g
    .selectAll('circle')
    .data(nodes)
    .enter()
    .append('circle')
    .attr('class', function (d) {
      return d.parent
        ? d.children
          ? 'node'
          : 'node node--leaf'
        : 'node node--root';
    })
    .style('fill', function (d) {
      if (d.data.name.startsWith('behavior')) {
        return '#3ad38d';
      } else if (d.parent === null) {
        return 'transparent';
      } else {
        return d.children ? color(d.depth) : null;
      }
    })
    .on('click', function (d) {
      if (focus !== d) zoom(d), d3.event.stopPropagation();
    });

  var text = g
    .selectAll('text')
    .data(nodes)
    .enter()
    .append('text')
    .attr('class', 'label')
    .style('fill-opacity', function (d) {
      return d.parent === root ? 1 : 0;
    })
    .style('display', function (d) {
      return d.parent === root ? 'inline' : 'none';
    })
    .style('font-size', function (d) {
      return 20 - d.depth * 3 + 'px';
    })
    .style('font-weight', 'bold')
    .text(function (d) {
      return d.data.name;
    });

  var node = g.selectAll('circle,text');

  svg.style('background', 'transparent').on('click', function () {
    zoom(root);
  });

  zoomTo([root.x, root.y, root.r * 2 + margin]);

  function zoom(d) {
    var focus0 = focus;
    focus = d;

    var transition = d3
      .transition()
      .duration(d3.event.altKey ? 7500 : 750)
      .tween('zoom', function (d) {
        var i = d3.interpolateZoom(view, [
          focus.x,
          focus.y,
          focus.r * 2 + margin,
        ]);
        return function (t) {
          zoomTo(i(t));
        };
      });

    transition
      .selectAll('text')
      .filter(function (d) {
        return d.parent === focus || this.style.display === 'inline';
      })
      .style('fill-opacity', function (d) {
        return d.parent === focus ? 1 : 0;
      })
      .on('start', function (d) {
        if (d.parent === focus) this.style.display = 'inline';
      })
      .on('end', function (d) {
        if (d.parent !== focus) this.style.display = 'none';
      });
  }

  function zoomTo(v) {
    var k = diameter / v[2];
    view = v;
    node.attr('transform', function (d) {
      return 'translate(' + (d.x - v[0]) * k + ',' + (d.y - v[1]) * k + ')';
    });
    circle.attr('r', function (d) {
      return d.r * k;
    });
  }
});

loadContentReward();
