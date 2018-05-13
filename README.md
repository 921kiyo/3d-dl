# Machine Learnig for Product Recognition at Ocado

## About the project

[Ocado](https://www.ocado.com) is an online supermarket delivering groceries to customers across the UK. Their warehouses are heavily automated to fulfill more than 250,000 orders a week from a range of over 50,000 products. However, not all parts of the warehouse are automated, and still requires manual labour and barcode scanners to recognise the products, and Ocado is interested in any new methods to speed up this process. 

The goal of the project is to deliver a machine learning system that can classify images of Ocado products in a range of environments.

Our approach is to generate 3D training images using the pipeline we developed, which consists of the following main components.

- 
- 
- 
- 


This project is conducted for  [Software Engineering Practice and Group project (CO 530)](http://www.imperial.ac.uk/computing/current-students/courses/530/), MSc in Computing Science at [Imperial College London](http://www.imperial.ac.uk/computing/).


The dataset is provided by [Ocado](https://www.ocado.com), 



**The full report of the project can be found [here](XX)**








# Table of Contents

* [Support](#support)
* [Release Types](#release-types)
* [Building Node.js](#building-nodejs)
* [Security](#security)
* [Project Team Members](##project-team-members)

<!-- ## Another paragraph <a name="paragraph2"></a> -->

## Support

Node.js contributors have limited availability to address general support
questions. Please make sure you are using a [currently-supported version of
Node.js](https://github.com/nodejs/Release#release-schedule).

When looking for support, please first search for your question in these venues:

* [Node.js Website][]
* [Node.js Help][]
* [Open or closed issues in the Node.js GitHub organization](https://github.com/issues?utf8=%E2%9C%93&q=sort%3Aupdated-desc+org%3Anodejs+is%3Aissue)

If you didn't find an answer in one of the official resources above, you can
search these unofficial resources:

* [Questions tagged 'node.js' on StackOverflow][]
* [#node.js channel on chat.freenode.net][]. See <http://nodeirc.info/> for more
  information.
* [Node.js Slack Community](https://node-js.slack.com/): Visit
  [nodeslackers.com](http://www.nodeslackers.com/) to register.

GitHub issues are meant for tracking enhancements and bugs, not general support.

Remember, libre != gratis; the open source license grants you the freedom to use
and modify, but not commitments of other people's time. Please be respectful,
and set your expectations accordingly.

## Release Types

The Node.js project maintains multiple types of releases:

* **Current**: Released from active development branches of this repository,
  versioned by [SemVer](https://semver.org) and signed by a member of the
  [Release Team](#release-team).
  Code for Current releases is organized in this repository by major version
  number. For example: [v4.x](https://github.com/nodejs/node/tree/v4.x).
  The major version number of Current releases will increment every 6 months
  allowing for breaking changes to be introduced. This happens in April and
  October every year. Current release lines beginning in October each year have
  a maximum support life of 8 months. Current release lines beginning in April
  each year will convert to LTS (see below) after 6 months and receive further
  support for 30 months.
* **LTS**: Releases that receive Long-term Support, with a focus on stability
  and security. Every second Current release line (major version) will become an
  LTS line and receive 18 months of _Active LTS_ support and a further 12
  months of _Maintenance_. LTS release lines are given alphabetically
  ordered codenames, beginning with v4 Argon. LTS releases are less frequent
  and will attempt to maintain consistent major and minor version numbers,
  only incrementing patch version numbers. There are no breaking changes or
  feature additions, except in some special circumstances.
* **Nightly**: Versions of code in this repository on the current Current
  branch, automatically built every 24-hours where changes exist. Use with
  caution.

More information can be found in the [LTS README](https://github.com/nodejs/LTS/).

### Download

Binaries, installers, and source tarballs are available at
<https://nodejs.org>.

#### Current and LTS Releases
**Current** and **LTS** releases are available at
<https://nodejs.org/download/release/>, listed under their version strings.
The [latest](https://nodejs.org/download/release/latest/) directory is an
alias for the latest Current release. The latest LTS release from an LTS
line is available in the form: latest-_codename_. For example:
<https://nodejs.org/download/release/latest-argon>.

#### Nightly Releases
**Nightly** builds are available at
<https://nodejs.org/download/nightly/>, listed under their version
string which includes their date (in UTC time) and the commit SHA at
the HEAD of the release.

#### API Documentation
**API documentation** is available in each release and nightly
directory under _docs_. <https://nodejs.org/api/> points to the API
documentation of the latest stable version.

### Verifying Binaries

Current, LTS, and Nightly download directories all contain a SHASUMS256.txt
file that lists the SHA checksums for each file available for
download.

The SHASUMS256.txt can be downloaded using `curl`.

```console
$ curl -O https://nodejs.org/dist/vx.y.z/SHASUMS256.txt
```

To check that a downloaded file matches the checksum, run
it through `sha256sum` with a command such as:

```console
$ grep node-vx.y.z.tar.gz SHASUMS256.txt | sha256sum -c -
```

Current and LTS releases (but not Nightlies) also have the GPG detached
signature of SHASUMS256.txt available as SHASUMS256.txt.sig. You can use `gpg`
to verify that SHASUMS256.txt has not been tampered with.

To verify SHASUMS256.txt has not been altered, you will first need to import
all of the GPG keys of individuals authorized to create releases. They are
listed at the bottom of this README under [Release Team](#release-team).
Use a command such as this to import the keys:

```console
$ gpg --keyserver pool.sks-keyservers.net --recv-keys DD8F2338BAE7501E3DD5AC78C273792F7D83545D
```

See the bottom of this README for a full script to import active release keys.

Next, download the SHASUMS256.txt.sig for the release:

```console
$ curl -O https://nodejs.org/dist/vx.y.z/SHASUMS256.txt.sig
```

After downloading the appropriate SHASUMS256.txt and SHASUMS256.txt.sig files,
you can then use `gpg --verify SHASUMS256.txt.sig SHASUMS256.txt` to verify
that the file has been signed by an authorized member of the Node.js team.

Once verified, use the SHASUMS256.txt file to get the checksum for
the binary verification command above.

<!-- ## Building Node.js

See [BUILDING.md](BUILDING.md) for instructions on how to build
Node.js from source. The document also contains a list of
officially supported platforms. -->

<!-- ### Private disclosure preferred

- [CVE-2016-7099](https://nodejs.org/en/blog/vulnerability/september-2016-security-releases/):
  _Fix invalid wildcard certificate validation check_. This is a high severity
  defect that would allow a malicious TLS server to serve an invalid wildcard
  certificate for its hostname and be improperly validated by a Node.js client.

- [#5507](https://github.com/nodejs/node/pull/5507): _Fix a defect that makes
  the CacheBleed Attack possible_. Many, though not all, OpenSSL vulnerabilities
  in the TLS/SSL protocols also affect Node.js.

- [CVE-2016-2216](https://nodejs.org/en/blog/vulnerability/february-2016-security-releases/):
  _Fix defects in HTTP header parsing for requests and responses that can allow
  response splitting_. While the impact of this vulnerability is application and
  network dependent, it is remotely exploitable in the HTTP protocol.

When in doubt, please do send us a report. -->


## Project Team Members <a name="project-team-members"></a>


<!-- * [watilde](https://github.com/watilde) -
**Daijiro Wachi** &lt;daijiro.wachi@gmail.com&gt; (he/him) -->
* [xxx](https://github.com/XXX) -
**Kiyohito Kunii** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Max Baylis** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Matthew Wong** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Ong Wai Hong** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Pavel Kroupa** &lt;XX@imperial.ac.uk&gt;
* [xxx](https://github.com/XXX) -
**Swen Koller** &lt;XX@imperial.ac.uk&gt;

## Contributing to Node.js

* [Contributing to the project][]
* [Working Groups][]
* [Strategic Initiatives][]

[Code of Conduct]: https://github.com/nodejs/admin/blob/master/CODE_OF_CONDUCT.md
[Contributing to the project]: CONTRIBUTING.md
[Node.js Help]: https://github.com/nodejs/help
[Node.js Website]: https://nodejs.org/en/
[Questions tagged 'node.js' on StackOverflow]: https://stackoverflow.com/questions/tagged/node.js
[Working Groups]: https://github.com/nodejs/TSC/blob/master/WORKING_GROUPS.md
[Strategic Initiatives]: https://github.com/nodejs/TSC/blob/master/Strategic-Initiatives.md
[#node.js channel on chat.freenode.net]: https://webchat.freenode.net?channels=node.js&uio=d4