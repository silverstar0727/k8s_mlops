import kfp

@kfp.components.func_to_container_op
def add_op(a: float, b: float) -> float:
    print(a, '+', b, '=', a + b)
    return a + b

@kfp.dsl.pipeline(
    name='Calculation pipeline',
    description='A toy pipeline that performs arithmetic calculations.'
)
def add_pipeline(
    a: float,
    b: float,
    c: float,
    d: float
):
    add_a_b = add_op(a, b)
    add_c_d = add_op(c, d)

    total = add_op(add_a_b.output, add_c_d.output)

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(pipeline_func=add_pipeline, package_path="add.zip")

# 파이프라인이 다운되는 이슈가 계속 발생
# https://github.com/kubeflow/pipelines/issues/1471