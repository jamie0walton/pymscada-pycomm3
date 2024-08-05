As of pymscada version 0.0.14 this is now part of the main package, so you do not need
to install this package to talk with Logix PLCs.

ARCHIVED.

# pymscada-pycomm3
Rockwell PLC driver for pymscada using pycomm3

```bash
cd                        # to location of config dir
cp {xxx}/site-packages/pymscada-pycomm3/demo/pycomm3.yaml config
vi config/pycomm3.yaml    # edit as appropriate for your site
vi config/tags.yaml       # add any tags
vi config/wwwserver.yaml  # add tags on web page
python -m pymscada_pycomm3
```

This will put Logix data on the [pymscada](https://github.com/jamie0walton/pymscada) bus as tag values.

