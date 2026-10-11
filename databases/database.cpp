#include <arrow/io/file.h>
#include <parquet/stream_writer.h>
#include <stdint.h>

int main()
{
   std::shared_ptr<arrow::io::FileOutputStream> outfile;

   PARQUET_ASSIGN_OR_THROW(
      outfile,
      arrow::io::FileOutputStream::Open("test.parquet"));

   parquet::WriterProperties::Builder builder;
   builder.compression(parquet::Compression::ZSTD);

   std::shared_ptr<parquet::schema::GroupNode> schema;
   parquet::schema::NodeVector fields;
   fields.push_back(parquet::schema::PrimitiveNode::Make(
       "POS_FUNCTOR", parquet::Repetition::REQUIRED, parquet::Type::BYTE_ARRAY, parquet::ConvertedType::UINT_32
   ));
   fields.push_back(parquet::schema::PrimitiveNode::Make(
       "WORD_ID", parquet::Repetition::REQUIRED, parquet::Type::BYTE_ARRAY, parquet::ConvertedType::UINT_32
   ));

    schema = std::static_pointer_cast<parquet::schema::GroupNode>(
   parquet::schema::GroupNode::Make("schema", parquet::Repetition::REQUIRED, fields));

   parquet::StreamWriter os{
      parquet::ParquetFileWriter::Open(outfile, schema, builder.build())};

    for (int i = 0; i < 1000; ++i)
    {
        os << "TESTCOL" << 3.14f << int32_t(100) << parquet::EndRow;
    }
}