FROM apps.fastgenomics.org/fastgenomics/base_calc_scanpy_py36:0.4.1 as base

VOLUME /fastgenomics/data
VOLUME /fastgenomics/output
VOLUME /fastgenomics/config
VOLUME /fastgenomics/summary

COPY manifest.json /app/
COPY calc_template /app/calc_template/

WORKDIR /app
RUN rm -rf write


FROM base as test

COPY sample_data /app/sample_data/
COPY tests       /app/tests/
COPY pytest.ini  /app/

ENV PYTHONPATH /app

RUN ["pip", "install", "pytest"]
RUN ["pytest", "--color=yes"]


FROM base AS final
CMD ["python", "-m", "calc_template"]
